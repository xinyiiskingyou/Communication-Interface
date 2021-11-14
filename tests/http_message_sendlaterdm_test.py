import pytest
import requests
import json
import time
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import create_dm, user1_send_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

# 1 second
TIME_WAIT = 1

##########################################
####### message/sendlaterdm/v1 tests #####
##########################################

# Input error: Invalid negative dm_id 
def test_sendlater_channel_neg(global_owner):
    token = global_owner['token']

    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': -1,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == INPUTERROR

# Input error: Invalid non-exist channel_id 
def test_sendlater_channel_non_exist(global_owner):
    token = global_owner['token']

    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': 256,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == INPUTERROR

# Over 1000 characters of message
def test_sendlater_long_msg(global_owner, register_user2, create_dm):
    token1 = global_owner['token']

    # Input error: long message
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': create_dm['dm_id'],
        'message': 'H' * 1001,
        'time_sent': time_sent
    })
    assert send.status_code == INPUTERROR

    # Aceess error: User not in dm + long message
    # User 1 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    assert dm.status_code == VALID

    dm_id = json.loads(dm.text)['dm_id']
    token2 = register_user2['token']
    send2 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'H' * 1001,
        'time_sent': time_sent
    })
    assert send2.status_code == ACCESSERROR

    # Access error: Invalid token + long message
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    send1 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': create_dm['dm_id'],
        'message': 'H' * 1001,
        'time_sent': time_sent
    })
    assert send1.status_code == ACCESSERROR

# Time_sent is in the past
def test_sendlater_past_time(global_owner, register_user2, create_dm):
    token1 = global_owner['token']

    # Input error: time_sent in the past
    time_sent = int(time.time()) - TIME_WAIT
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': create_dm['dm_id'],
        'message': 'Hello, World!',
        'time_sent': time_sent
    })
    assert send.status_code == INPUTERROR

    # Aceess error: User not in channel + time_sent in the past
    # User 1 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    assert dm.status_code == VALID

    dm_id = json.loads(dm.text)['dm_id']
    token2 = register_user2['token']
    send2 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'Hello, World!',
        'time_sent': time_sent
    })
    assert send2.status_code == ACCESSERROR

    # Access error: Invalid token + time_sent in the past
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    send1 = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': create_dm['dm_id'],
        'message': 'Hello, World!',
        'time_sent': time_sent
    })
    assert send1.status_code == ACCESSERROR

# Acess error: auth_user not in the channel
def test_sendlater_user_not_channel(global_owner,register_user2):
    token1 = global_owner['token']
    token2 = register_user2['token']
    time_sent = TIME_WAIT + int(time.time())

    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token1,
        'u_ids': []
    })
    assert dm.status_code == VALID

    dm_id = json.loads(dm.text)['dm_id']
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token2,
        'dm_id': dm_id,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == ACCESSERROR

# Access error: invalid token
def test_sendlater_invalid_token(global_owner, create_dm):
    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': create_dm['dm_id'],
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == ACCESSERROR

# Access error: Global owner is not the member of the channel
def test_sendlater_global_owner(global_owner, register_user2):
    token = global_owner['token']

    # User 2 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': register_user2['token'],
        'u_ids': []
    })
    assert dm.status_code == VALID

    dm_id = json.loads(dm.text)['dm_id']
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': dm_id,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == ACCESSERROR

##### Implementation #####
def test_sendlater_valid_owner(global_owner, create_dm):

    token = global_owner['token']
    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token,
        'dm_id': create_dm['dm_id'],
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == VALID

def test_sendlater_valid_invite_user(global_owner, register_user2):
    token1 = global_owner['token']
    u_id = global_owner['auth_user_id']
    token2 = register_user2['token']

    # User 2 creates dm
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token2,
        'u_ids': [u_id]
    })
    assert dm.status_code == VALID

    dm_id = json.loads(dm.text)['dm_id']

    time_sent = TIME_WAIT + int(time.time())
    send = requests.post(config.url + "message/sendlaterdm/v1", json = {
        'token': token1,
        'dm_id': dm_id,
        'message': 'Hello world!',
        'time_sent': time_sent
    })
    assert send.status_code == VALID
