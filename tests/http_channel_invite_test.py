import pytest
import requests
import json
from src import config 

##########################################
########## channel_invite tests ##########
##########################################

# Invalid u_id
def test_invite_invalid_u_id():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': token,
        'name': 'anna',
        'is_public': True
    })

    channel_id1 = json.loads(channel.text)['channel_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id1,
        'u_id': -16
    })
    assert invite.status_code == 400

# Invalid channel_id
def test_invite_invalid_channel_id():
    requests.delete(config.url + "clear/v1")

    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    u_id = user1_data['auth_user_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': -16,
        'u_id': u_id
    })
    assert invite.status_code == 400

def test_invite_already_member():
    requests.delete(config.url + "clear/v1")

    # create a user that has channel
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    token = user_data['token']

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    # create 2 users that don't have channels
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token1 = user1_data['token']
    u_id = user1_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    # test error when channel_id is valid but authorised user is not a member of the channel
    channel_invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    })

    assert channel_invite.status_code == 403

    # now let user1 join the channel
    join = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert join.status_code == 200

    # test error when u_id refers to a user who is already a member of the channel
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 400

def test_valid_channel_invite():
    requests.delete(config.url + "clear/v1")

    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    token = user_data['token']

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user2_data = user2.json()
    u_id = user2_data['auth_user_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert invite.status_code == 200

