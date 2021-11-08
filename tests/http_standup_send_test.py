import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

###############################################
########### standup_send tests ###############
###############################################

# Access error: invalid token
def test_standup_send_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'hihi'
    })
    assert send.status_code == ACCESSERROR

# Input Error: invalid channel_id
def test_standup_send_invalid_channel_id(global_owner):
    token = global_owner['token']

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': -1,
        'message': 'hihi'
    })
    assert send.status_code == INPUTERROR

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': 256,
        'message': 'hihi'
    })
    assert send.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': -256,
        'message': 'hihi'
    })
    assert send.status_code == ACCESSERROR

# Input error: length of message is over 1000 characters
def test_standup_send_invalid_message_length(global_owner, create_channel, register_user2):

    token = global_owner['token']
    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'a' * 1001
    })
    assert send.status_code == INPUTERROR

    # Access error: invalid token and invalid length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'a' * 1001
    })
    assert send.status_code == ACCESSERROR

    # Access error: invalid length and user is not a member of channel
    send = requests.post(config.url + "standup/send/v1", json = {
        'token': register_user2['token'],
        'channel_id': create_channel['channel_id'],
        'message': 'a' * 1001
    })
    assert send.status_code == ACCESSERROR

# Input error: an active standup is not currently running in the channel
def test_standup_send_not_active(global_owner, create_channel, register_user2):
    
    token = global_owner['token']
    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'hihihi'
    })
    assert send.status_code == INPUTERROR

    # Access error: invalid token and invalid length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': -256,
        'message': 'hiiii'
    })
    assert send.status_code == ACCESSERROR

    # Access error: invalid length and user is not a member of channel
    send = requests.post(config.url + "standup/send/v1", json = {
        'token': register_user2['token'],
        'channel_id': create_channel['channel_id'],
        'message': 'hiii'
    })
    assert send.status_code == ACCESSERROR

# Access error: user is not a member of the channel
def test_standup_send_user_not_member(global_owner, create_channel, register_user2):

    token = register_user2['token']

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'hihi'
    })
    assert send.status_code == ACCESSERROR
