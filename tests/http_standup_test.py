import pytest
import json 
import requests
from src import config
from tests.fixture import VALID, INPUTERROR, ACCESSERROR
from tests.fixture import global_owner, create_channel

####ERROR TESTS FOR ALL STANDUP FUNCTIONS### 


##STANDUP START### 
def test_standup_invalid_channel_id(global_owner):
    token1 = global_owner['token']

    # Test invalid channel_id
    resp1 = requests.get(config.url + "standup/start/v1", params = {
        'token': token1,
        'channel_id': -1,
        'length': 1
    })

    resp2 = requests.get(config.url + "standup/start/v1", params = {
        'token': token1,
        'channel_id': 0,
        'length': 1
    })

    resp3 = requests.get(config.url + "standup/start/v1", params = {
        'token': token1,
        'channel_id': 256,
        'length': 1
    })

    assert resp1.status_code == INPUTERROR
    assert resp2.status_code == INPUTERROR
    assert resp3.status_code == INPUTERROR

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token1,
        'channel_id': 256,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR


def test_standup_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    channel = create_channel['channel_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token,
        'channel_id': channel,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR

def test_standup_negative_length(global_owner, create_channel): 
    token = global_owner['token']
    channel = create_channel['channel_id']
    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token,
        'channel_id': channel,
        'length': -1
    })
    assert resp1.status_code == INPUTERROR



###STANDUP ACTIVE### 
def test_standup_active_invalid_channel(): 
    token1 = global_owner['token']

    # Test invalid channel_id
    resp1 = requests.get(config.url + "standup/active/v1", params = {
        'token': token1,
        'channel_id': -1,
        'length': 1
    })

    resp2 = requests.get(config.url + "standup/active/v1", params = {
        'token': token1,
        'channel_id': 0,
        'length': 1
    })

    resp3 = requests.get(config.url + "standup/active/v1", params = {
        'token': token1,
        'channel_id': 256,
        'length': 1
    })

    assert resp1.status_code == INPUTERROR
    assert resp2.status_code == INPUTERROR
    assert resp3.status_code == INPUTERROR

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token1,
        'channel_id': 256,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR


def test_standup_active_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    channel = create_channel['channel_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token,
        'channel_id': channel,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR


def test_standup_valid(global_owner, create_channel):
    token = global_user['token']
    channel = create_channel['channel_id']

    start = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel,
        'length': 10
    })
    assert start.status_code == VALID

    send1 = requests.post(config.url + "standup/send/v1", json = { 
        'token': token, 
        'channel_id': channel,
        'message': helohelo 
    })
    assert send1.status_code == VALID
    send2 = requests.post(config.url + "standup/send/v1", json = { 
        'token': token, 
        'channel_id': channel,
        'message': helohelomelo 
    })
    assert send2.status_code == VALID

