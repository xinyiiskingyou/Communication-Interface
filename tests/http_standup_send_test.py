import time
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

# Valid case: sending one message in standup
def test_standup_valid_message(global_owner, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    assert json.loads(resp1.text)['time_finish'] != 0

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message1'
    })
    assert send.status_code == VALID

    #time.sleep(3)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert json.loads(message.text)['messages'] == 'annalee: message1\n'''
    
# Valid case: sending more messages in standup
def test_standup_valid_more_messages(global_owner, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    assert json.loads(resp1.text)['time_finish'] != 0

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message1'
    })
    assert send.status_code == VALID

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message2'
    })
    assert send.status_code == VALID

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message3'
    })
    assert send.status_code == VALID

    time.sleep(3)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert json.loads(message.text)['messages'] == 'annalee: message1\nannalee: message2\nannalee: message3\n'
