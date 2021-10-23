import pytest
import requests
import json
from src import config

@pytest.fixture
def register_user1():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        'email': 'anna@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    return user_data

# user 1 cerates a channel
@pytest.fixture
def user1_channel_id(register_user1):

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': register_user1['token'],
        'name': 'anna_channel',
        'is_public': False
    })
    channel_data = channel.json()
    return channel_data['channel_id']

@pytest.fixture
def register_user2():
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    return user2_data

##########################################
########## message/send/v1 tests #########
##########################################
def test_message_send_invalid_token(register_user1, user1_channel_id):

    token = register_user1['token']
    channel1_id = user1_channel_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': token,
        'channel_id': channel1_id, 
        'message': 'hello there'
    })
    assert send_message.status_code == 403

# Input Error when channel_id does not refer to a valid channel
# Channel id is negative
def test_message_send_invalid_channel_id_negative(register_user1):

    user1_token = register_user1['token']

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': -1, 
        'message': 'hello there'
    })
    assert send_message.status_code == 400

    # invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': -1, 
        'message': 'hello there'
    })
    assert send_message.status_code == 403
    
# Input Error when channel_id does not refer to a valid channel
# id is positive integer, but is not an id to any channel
def test_message_send_invalid_channel_id_nonexistant(register_user1):

    user1_token = register_user1['token']

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
    assert send_message.status_code == 400

    # invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': 256, 
        'message': 'hello there'
    })
    assert send_message.status_code == 403

# Input error when length of message is less than 1 or over 1000 characters
def test_message_send_invalid_message(register_user1, user1_channel_id):

    user1_token = register_user1['token']
    channel1_id = user1_channel_id

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'a' * 1001
    })
    assert send_message1.status_code == 400

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': ''
    })
    assert send_message2.status_code == 400

    # invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': 256, 
        'message': 'a' * 1001
    })
    assert send_message.status_code == 403

# Access error when channel_id is valid and the authorised user 
# is not a member of the channel
def test_message_send_unauthorised_user(register_user1, register_user2, user1_channel_id):

    user1_token = register_user1['token']
    user2_token = register_user2['token']
    assert user1_token != user2_token

    channel1_id = user1_channel_id

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'message': 'hello there'
    })
    assert send_message1.status_code == 403

##### Implementation #####

# Send message in one channel by two users
def test_message_send_valid_one_channel(register_user1, user1_channel_id, register_user2):

    user1_token = register_user1['token']

    # User 1 creates channel 1
    channel1_id = user1_channel_id

    # User 1 sends message 1 in channel 1
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'hello there'
    })
    assert send_message1.status_code == 200
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
    assert send_message2.status_code == 200
    assert message_id1 != message_id2

# Send message in two channels and compare message_id to 
# ensure different message_id's across different channels
def test_message_send_valid_two_channel(register_user1, user1_channel_id, register_user2):
    # Register user 1
    user1_token = register_user1['token']
    u_id1 = register_user1['auth_user_id']

    # User 1 creates channel 1
    channel1_id = user1_channel_id

    # User 1 sends message 1 in channel 1
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'hello there'
    })
    assert send_message1.status_code == 200
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
    assert send_message3.status_code == 200
