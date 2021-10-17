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
def register_user1():

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
def test_invite_invalid_u_id(register_user, register_user1, create_channel):

    token = register_user['token']
    channel = create_channel['channel_id']

    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': channel,
        'u_id': -16
    })
    assert invite.status_code == 400

    # Access error channel_id is valid and authorised user is not a member of the channel
    # and the u_id is invalid
    user2_token = register_user1['token']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user2_token,
        'channel_id': channel,
        'u_id': -16
    })
    assert invite.status_code == 403

# Invalid channel_id
def test_invite_invalid_channel_id(register_user, register_user1):

    user_token = register_user['token']
    u_id = register_user1['auth_user_id']

    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user_token,
        'channel_id': -16,
        'u_id': u_id
    })
    assert invite.status_code == 400
    
def test_invite_already_member(register_user, create_channel, register_user1):
    requests.delete(config.url + "clear/v1")

    # create a user that has channel
    user1_token = register_user['token']
    user1_id = register_user['auth_user_id']
    channel_id = create_channel['channel_id']

    # create 2 users that don't have channels
    user2_id = register_user1['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user3_data = user3.json()
    user3_token = user3_data['token']

    # test error when channel_id is valid but authorised user is not a member of the channel
    channel_invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user3_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert channel_invite.status_code == 403

    # test error when u_id refers to a user who is already a member of the channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })
    assert invite.status_code == 400

def test_valid_channel_invite(register_user, create_channel, register_user1):

    token = register_user['token']
    channel_id = create_channel['channel_id']
    # invite an user that is not a member of the channel
    u_id = register_user1['auth_user_id']

    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert invite.status_code == 200
