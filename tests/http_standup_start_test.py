import pytest
import requests
import json
import time
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

###############################################
########## standup_start tests ################
###############################################

# AccessError: invalid token
def test_standup_start_invalid_token(global_owner, create_channel):
    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    start = requests.post(config.url + "standup/start/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'length': 1
    })
    assert start.status_code == ACCESSERROR

# Input error: invalid channel_id
def test_standup_start_invalid_channel_id(global_owner):
    token1 = global_owner['token']

    # Test invalid channel_id
    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': -1,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR

    resp2 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': 256,
        'length': 1
    })
    assert resp2.status_code == INPUTERROR

    # Acess error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': 256,
        'length': 1
    })
    assert resp1.status_code == ACCESSERROR

# Input error: length is a negative integer
def test_standup_start_invalid_length(global_owner, create_channel, register_user2):
    token1 = global_owner['token']

    # Test invalid channel_id
    resp1 = requests.post(config.url + "standup/start/v1", json = {
        'token': token1,
        'channel_id': create_channel['channel_id'],
        'length': -1
    })
    assert resp1.status_code == INPUTERROR

    # Test invalid channel_id
    resp1 = requests.post(config.url + "standup/start/v1", json = {
        'token': token1,
        'channel_id': create_channel['channel_id'],
        'length': -1000
    })
    assert resp1.status_code == INPUTERROR

    # Access error: invalid token and invalid length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': create_channel['channel_id'],
        'length': -1
    })
    assert resp1.status_code == ACCESSERROR

    # Access error: invalid length and user is not a member of channel
    resp1 = requests.post(config.url + "standup/start/v1", json = {
        'token': register_user2['token'],
        'channel_id': create_channel['channel_id'],
        'length': -1
    })
    assert resp1.status_code == ACCESSERROR

def test_standup_already_active(global_owner, create_channel):

    channel_id = create_channel['channel_id']
    token1 = global_owner['token']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR
    time.sleep(2)

# Access error: user is not a member of channel
def test_standup_user_not_member(global_owner, register_user2, create_channel):

    channel_id = create_channel['channel_id']
    token1 = register_user2['token']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token1,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == ACCESSERROR

# Valid case: start a standup but do not send any messages
def test_standup_valid_no_message(global_owner, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    assert json.loads(resp1.text)['time_finish'] != None
    time.sleep(2)
