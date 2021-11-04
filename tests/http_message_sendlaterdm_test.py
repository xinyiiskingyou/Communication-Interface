import pytest
import requests
import json
import time
from src import config

# 10 minute
TIME_WAIT = 3
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

# user1 creates a dm with user2 
@pytest.fixture
def user1_dm(register_user1, register_user2):
    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': register_user1['token'],
        'u_ids': [register_user2['auth_user_id']]
    })
    assert create_dm1.status_code == 200
    dm_id = json.loads(create_dm1.text)['dm_id']
    return dm_id

# Input error: Invalid negative dm_id 
def test_sendlater_channel_neg(register_user1):
    token = register_user1['token']

    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': -1,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 400

# Input error: Invalid non-exist channel_id 
def test_sendlater_channel_non_exist(register_user1):
    token = register_user1['token']

    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': 256,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 400

# Over 1000 characters of message
def test_sendlater_long_msg(register_user1, register_user2, user1_dm):
    token1 = register_user1['token']

    # Input error: long message
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': user1_dm,
        'message': 'H' * 1001,
        'time_sent': time_sent
    })
    assert send.status_code == 400

    # Aceess error: User not in dm + long message
    # User 1 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    assert dm.status_code == 200

    dm_id = json.loads(dm.text)['dm_id']
    token2 = register_user2['token']
    send2 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'H' * 1001,
        'time_sent': time_sent
    })
    assert send2.status_code == 403

    # Access error: Invalid token + long message
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    send1 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': user1_dm,
        'message': 'H' * 1001,
        'time_sent': time_sent
    })
    assert send1.status_code == 403


# Time_sent is in the past
def test_sendlater_past_time(register_user1, register_user2, user1_dm):
    token1 = register_user1['token']

    # Input error: time_sent in the past
    time_sent = int(time.time()) - TIME_WAIT
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': user1_dm,
        'message': 'Hello, World!',
        'time_sent': time_sent
    })
    assert send.status_code == 400

    # Aceess error: User not in channel + time_sent in the past
    # User 1 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    assert dm.status_code == 200

    dm_id = json.loads(dm.text)['dm_id']
    token2 = register_user2['token']
    send2 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'Hello, World!',
        'time_sent': time_sent
    })
    assert send2.status_code == 403

    # Access error: Invalid token + time_sent in the past
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    send1 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': user1_dm,
        'message': 'Hello, World!',
        'time_sent': time_sent
    })
    assert send1.status_code == 403

# Acess error: auth_user not in the channel
def test_sendlater_user_not_channel(register_user1,register_user2):
    token1 = register_user1['token']
    token2 = register_user2['token']
    time_sent = TIME_WAIT + int(time.time())

    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    assert dm.status_code == 200

    dm_id = json.loads(dm.text)['dm_id']
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 403

# Access error: invalid token
def test_sendlater_invalid_token(register_user1, user1_dm):
    token = register_user1['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': user1_dm,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 403

# Access error: Global owner is not the member of the channel
def test_sendlater_global_owner(register_user1, register_user2):
    token = register_user1['token']

    # User 2 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': register_user2['token'],
        'u_ids': []
    })
    assert dm.status_code == 200

    dm_id = json.loads(dm.text)['dm_id']
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': dm_id,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 403

##### Implementation #####
def test_sendlater_valid_owner(register_user1, user1_dm):
    token = register_user1['token']
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': user1_dm,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 200

def test_sendlater_valid_invite_user(register_user1, register_user2):
    token1 = register_user1['token']
    u_id = register_user1['auth_user_id']
    token2 = register_user2['token']

    # User 2 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token2,
        'u_ids': [u_id]
    })
    assert dm.status_code == 200

    dm_id = json.loads(dm.text)['dm_id']

    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': dm_id,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == 200
