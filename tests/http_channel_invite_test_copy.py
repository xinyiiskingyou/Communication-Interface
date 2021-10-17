import pytest
import requests
import json
from src import config 

##########################################
########## channel_invite tests ##########
##########################################

@pytest.fixture
def register_user():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user2():

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    return user1_data

@pytest.fixture
def create_channel(register_user):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user['token'],
        'name': 'anna',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data

# Invalid u_id
def test_invite_invalid_u_id(register_user, create_channel):

    token = register_user['token']
    channel = create_channel['channel_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel,
        'u_id': -16
    })
    assert invite.status_code == 400

# Invalid channel_id
def test_invite_invalid_channel_id(register_user, register_user2):

    token = register_user['token']
    u_id = register_user2['auth_user_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': -16,
        'u_id': u_id
    })
    assert invite.status_code == 400

def test_invite_already_member(register_user, create_channel, register_user2):
    requests.delete(config.url + "clear/v1")

    # create a user that has channel
    token = register_user['token']
    u_id1 = register_user['auth_user_id']
    channel_id = create_channel['channel_id']

    # create 2 users that don't have channels
    u_id = register_user2['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user2_data = user2.json()
    token2 = user2_data['token']

    # test error when channel_id is valid but authorised user is not a member of the channel
    channel_invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert channel_invite.status_code == 403

    # test error when u_id refers to a user who is already a member of the channel
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id1
    })
    assert invite.status_code == 400

def test_valid_channel_invite(register_user, create_channel, register_user2):

    token = register_user['token']
    channel_id = create_channel['channel_id']
    # invite an user that is not a member of the channel
    u_id = register_user2['auth_user_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert invite.status_code == 200

