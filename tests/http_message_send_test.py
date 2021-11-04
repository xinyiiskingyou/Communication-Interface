import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########## message/send/v1 tests #########
##########################################
def test_message_send_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    channel1_id = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': token,
        'channel_id': channel1_id, 
        'message': 'hello there'
    })
    assert send_message.status_code == ACCESSERROR

# Input Error when channel_id does not refer to a valid channel
# Channel id is negative
def test_message_send_invalid_channel_id_negative(global_owner):

    user1_token = global_owner['token']

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': -1, 
        'message': 'hello there'
    })
    assert send_message.status_code == INPUTERROR

    # invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': -1, 
        'message': 'hello there'
    })
    assert send_message.status_code == ACCESSERROR
    
# Input Error when channel_id does not refer to a valid channel
# id is positive integer, but is not an id to any channel
def test_message_send_invalid_channel_id_nonexistant(global_owner):

    user1_token = global_owner['token']

    requests.post(config.url + "channels/create/v2", json = {
        'token': user1_token,
        'name': 'anna_channel',
        'is_public': False
    })

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': 256, 
        'message': 'hello there'
    })
    assert send_message.status_code == INPUTERROR

    # invalid token
    requests.post(config.url + "auth/logout/v1", json ={
        'token': user1_token
    })
    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': 256, 
        'message': 'hello there'
    })
    assert send_message.status_code == ACCESSERROR

# Input error when length of message is less than 1 or over 1000 characters
def test_message_send_invalid_message(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'a' * 1001
    })
    assert send_message1.status_code == INPUTERROR

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': ''
    })
    assert send_message2.status_code == INPUTERROR

    # invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': 256, 
        'message': 'a' * 1001
    })
    assert send_message.status_code == ACCESSERROR

# Access error when channel_id is valid and the authorised user 
# is not a member of the channel
def test_message_send_unauthorised_user(global_owner, register_user2, create_channel):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    assert user1_token != user2_token

    channel1_id = create_channel['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'message': 'hello there'
    })
    assert send_message1.status_code == ACCESSERROR

##### Implementation #####

# Send message in one channel by two users
def test_message_send_valid_one_channel(global_owner, create_channel, register_user2):

    user1_token = global_owner['token']

    # User 1 creates channel 1
    channel1_id = create_channel['channel_id']

    # User 1 sends message 1 in channel 1
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'hello there'
    })
    assert send_message1.status_code == VALID
    message_id1 = json.loads(send_message1.text)['message_id']

    # Register user 2
    user2_token = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 invites user 2 to channel 1
    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'u_id': u_id2
    })

    # User 2 sends a message in channel 1
    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'message': 'general kenobi'
    })
    message_id2 = json.loads(send_message2.text)['message_id']
    
    assert send_message2.status_code == VALID
    assert message_id1 != message_id2

# Send message in two channels and compare message_id to 
# ensure different message_id's across different channels
def test_message_send_valid_two_channel(global_owner, create_channel, register_user2):
    # Register user 1
    user1_token = global_owner['token']
    u_id1 = global_owner['auth_user_id']

    # User 1 creates channel 1
    channel1_id = create_channel['channel_id']

    # User 1 sends message 1 in channel 1
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'hello there'
    })
    assert send_message1.status_code == VALID
    message_id1 = json.loads(send_message1.text)['message_id']

    # Register user 2
    user2_token = register_user2['token']

    # User 2 creates channel 2
    channel2 = requests.post(config.url + "channels/create/v2", json = {
        'token': user2_token,
        'name': 'sally_channel',
        'is_public': True
    })
    channel2_id = json.loads(channel2.text)['channel_id']

    # User 2 invites user 1 to channel 2
    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user2_token,
        'channel_id': channel2_id,
        'u_id': u_id1
    })

    # User 1 sends a message in channel 2
    send_message3 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel2_id,
        'message': 'hello there'
    })

    message_id3 = json.loads(send_message3.text)['message_id']
    assert message_id1 !=  message_id3
    assert send_message3.status_code == VALID
