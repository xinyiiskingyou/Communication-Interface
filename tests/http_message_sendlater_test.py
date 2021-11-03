import pytest
import requests
import json
from src import config
TIME_SENT = 60
@pytest.fixture
def register_user1():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        'email': 'anna@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user2():
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'sallly@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    return user2_data

# user1 cerates a channel
@pytest.fixture
def user1_channel_id(register_user1):
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': register_user1['token'],
        'name': 'anna_channel',
        'is_public': False
    })
    channel_data = channel.json()
    return channel_data['channel_id']

# Input error: Invalid negative channel_id 
def test_sendlater_channel_neg(register_user1):
    token = register_user1['token']

    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': -1,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 400

# Input error: Invalid non-exist channel_id 
def test_sendlater_channel_non_exist(register_user1):
    token = register_user1['token']

    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': 256,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 400

# Over 1000 characters of message
def test_sendlater_long_msg(register_user1, register_user2, user1_channel_id):
    token1 = register_user1['token']

    # Input error: long message
    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token1,
        'channel_id': user1_channel_id,
        'message': 'Hello world!' * 1000,
        'time_sent': TIME_SENT
    })
    assert send.status_code == 400

    # Access error: Invalid token + long message
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    send1 = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token1,
        'channel_id': user1_channel_id,
        'message': 'Hello world!' * 1000,
        'time_sent': TIME_SENT
    })
    assert send1.status_code == 403

    # Aceess error: User not in channel + long message
    token2 = register_user2['token']
    send2 = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token2,
        'channel_id': user1_channel_id,
        'message': 'Hello world!' * 1000,
        'time_sent': TIME_SENT
    })
    assert send2.status_code == 403

# Acess error: auth_user not in the channel
def test_sendlater_user_not_channel(register_user2, user1_channel_id):
    token = register_user2['token']
    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': user1_channel_id,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 403

# Access error: invalid token
def test_sendlater_invalid_token(register_user1, user1_channel_id):
    token = register_user1['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': user1_channel_id,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 403

# Access error: Global owner is not the member of the channel
def test_sendlater_global_owner(register_user1, register_user2):
    token = register_user1['token']

    # User 2 creates channel 2
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': register_user2['token'],
        'name': 'sally_channel',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']
    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': channel1_id,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 403

##### Implementation #####
def test_sendlater_valid_owner(register_user1, user1_channel_id):
    token = register_user1['token']

    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': user1_channel_id,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 200

def test_sendlater_valid_invite_user(register_user1, register_user2, user1_channel_id):
    token = register_user1['token']
    u_id = register_user2['auth_user_id']
    token2 = register_user2['token']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': user1_channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 200

    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token2,
        'channel_id': user1_channel_id,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 200

def test_sendlater_valid_join_user(register_user1, register_user2):
    token = register_user1['token']

    # User 2 creates channel 2
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': register_user2['token'],
        'name': 'sally_channel',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    join = requests.post(config.url + "channel/join/v2", json ={
        'token': token,
        'channel_id': channel_id
    })
    assert join.status_code == 200

    send = requests.post(config.url + "message/sendlater/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'message': 'Hello world!',
        'time_sent': TIME_SENT
    })
    assert send.status_code == 200