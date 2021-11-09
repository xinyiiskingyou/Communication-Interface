import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

###############################################
########## standup_active tests ###############
###############################################

# Access error: invalid token
def test_standup_active_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    active = requests.get(config.url + "standup/active/v1", params = {
        'token': token,
        'channel_id': create_channel['channel_id'],
    })
    assert active.status_code == ACCESSERROR

# Input error: invalid channel_id
def test_standup_active_invalid_channel_id(global_owner): 
    token1 = global_owner['token']

    # Test invalid channel_id
    resp1 = requests.get(config.url + "standup/active/v1", params = {
        'token': token1,
        'channel_id': -1,
    })
    assert resp1.status_code == INPUTERROR

    resp2 = requests.get(config.url + "standup/active/v1", params = {
        'token': token1,
        'channel_id': 256,
    })

    assert resp2.status_code == INPUTERROR

    # Access error: invalid token and invalid channel id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token1,
        'channel_id': 256,
    })
    assert resp1.status_code == ACCESSERROR

# Access error: user is not a member of channel
def test_standup_user_not_member(global_owner, register_user3, create_channel):

    token1 = register_user3['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token1,
        'channel_id': channel_id,
    })
    assert resp1.status_code == ACCESSERROR

def test_standup_valid_not_active(global_owner, create_channel):
    token = global_owner['token']

    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
    })
    assert resp1.status_code == VALID

    #assert json.loads(resp1.text)['is_active'] == False
    #assert json.loads(resp1.text)['time_finish'] == None

def test_standup_valid_active(global_owner, create_channel):
    token = global_owner['token']

    start = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'length': 1
    })
    assert start.status_code == VALID

    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
    })
    assert resp1.status_code == VALID

    #assert json.loads(resp1.text)['is_active'] == True
    #assert json.loads(resp1.text)['time_finish'] != None

    