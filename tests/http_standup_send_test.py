import re
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

    time.sleep(5)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert json.loads(message.text)['messages'][0]['message'] == 'annalee: message1\n'
    
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

    time.sleep(5)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert json.loads(message.text)['messages'][0]['message'] == 'annalee: message1\nannalee: message2\nannalee: message3\n'

# Valid case: react and unreact to a standup message
def test_standup_valid_react_standup(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message3'
    })
    assert send.status_code == VALID

    time.sleep(5)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    message_id = json.loads(message.text)['messages'][0]['message_id']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': token,
        'message_id': message_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert json.loads(message.text)['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': token,
        'message_id': message_id,
        'react_id': 1
    })
    assert unreact.status_code == VALID

    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert json.loads(message.text)['messages'][0]['reacts'][0]['is_this_user_reacted'] == False

# Valid case: pin and unpin to a standup message
def test_standup_valid_pin_standup(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message3'
    })
    assert send.status_code == VALID

    time.sleep(5)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    message_id = json.loads(message.text)['messages'][0]['message_id']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': token,
        'message_id': message_id,
    })
    assert pin.status_code == VALID

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': token,
        'channel_id': channel_id,
        'start': 0
    })
    pinned = json.loads(messages.text)['messages'][0]['is_pinned']
    assert pinned == True

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': token,
        'message_id': message_id,
    })
    assert unpin.status_code == VALID

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': token,
        'channel_id': channel_id,
        'start': 0
    })
    pinned = json.loads(messages.text)['messages'][0]['is_pinned']
    assert pinned == False

# Valid case: remove and edit the standup message
def test_standup_valid_edit_standup(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message3'
    })
    assert send.status_code == VALID

    time.sleep(5)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    message_id = json.loads(message.text)['messages'][0]['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': token,
        'message_id': message_id,
        'message': 'naninaninani'
    })
    assert edit_message.status_code == VALID

    remove_message = requests.delete(config.url + "message/remove/v1", json = {
        'token': token,
        'message_id': message_id,
    })
    assert remove_message.status_code == VALID

    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert len(json.loads(message.text)['messages']) == 0

# Valid case: share a standup message
def test_standup_valid_share_standup(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "standup/start/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'length': 1
    })
    assert resp1.status_code == VALID

    send = requests.post(config.url + "standup/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'],
        'message': 'message3'
    })
    assert send.status_code == VALID

    time.sleep(5)
    message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    message_id = json.loads(message.text)['messages'][0]['message_id']

    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': token,
        'og_message_id': message_id,
        'message': '', 
        'channel_id': create_channel['channel_id'],
        'dm_id': -1
    })
    assert share_message1.status_code == VALID
