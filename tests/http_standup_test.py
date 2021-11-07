import pytest
import json 
from src.error import AccessError, InputError
import requests
from src import config
import fixture 

####ERROR TESTS FOR ALL STANDUP FUNCTIONS### 


##STANDUP START### 
def test_standup_invalid_channel_id(register_user):
    token1 = register_user['token']

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


def test_standup_invalid_token(register_user, create_public_channel):

    token = register_user['token']
    channel = create_public_channel['channel_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token,
        'channel_id': channel,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR

def test_standup_negative_length(register_user, create_public_channel): 
    token = register_user['token']
    channel = create_public_channel['channel_id']
    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token,
        'channel_id': channel,
        'length': -1
    })
    assert resp1.status_code == INPUTERROR



###STANDUP ACTIVE### 
def test_standup_active_invalid_channel(): 
    token1 = register_user['token']

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


def test_standup_active_invalid_token(register_user, create_public_channel):

    token = register_user['token']
    channel = create_public_channel['channel_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "standup/active/v1", params ={
        'token': token,
        'channel_id': channel,
        'length': 1
    })
    assert resp1.status_code == INPUTERROR


    