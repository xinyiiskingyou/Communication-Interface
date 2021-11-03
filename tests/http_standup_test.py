import pytest
import json 
from src.error import AccessError, InputError
import requests
from src import config
##import a fixture file(probably xinyi made it) 

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
def create_public_channel(register_user):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data


def test_standup_invalid_channel_id(register_user):
 
    token1 = register_user['token']

    # Test invalid channel_id
    resp1 = requests.get(config.url + "standup/start/v1", params = {
        'token': token1,
        'channel_id': -1
    })

    resp2 = requests.get(config.url + "standup/start/v1", params = {
        'token': token1,
        'channel_id': 0
    })

    resp3 = requests.get(config.url + "standup/start/v1", params = {
        'token': token1,
        'channel_id': 256
    })

    assert resp1.status_code == 400
    assert resp2.status_code == 400
    assert resp3.status_code == 400

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token1,
        'channel_id': 256
    })
    assert resp1.status_code == 403


def test_standup_invalid_token(register_user, create_public_channel):

    token = register_user['token']
    channel = create_public_channel['channel_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "standup/start/v1", params ={
        'token': token,
        'channel_id': channel
    })
    assert resp1.status_code == 403