import pytest
import requests
import json
from src import config

@pytest.fixture
def setup():
    requests.delete(config.url + "clear/v1")

##########################################
########## message/send/v1 tests #########
##########################################

# Input Error when channel_id does not refer to a valid channel
# Channel id is negative
def test_message_send_invalid_channel_id_negative(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    send_message = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': -1, 
            'message': 'hello there'
        }
    )
    assert send_message.status_code == 400


# Input Error when channel_id does not refer to a valid channel
# id is positive integer, but is not an id to any channel
def test_message_send_invalid_channel_id_nonexistant(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )

    channel2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user2_token,
            'name': 'sally_channel',
            'is_public': False
        }
    )

    send_message = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': 256, 
            'message': 'hello there'
        }
    )
    assert send_message.status_code == 400


# Input error when length of message is less than 1 or over 1000 characters
def test_message_send_invalid_message(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'a' * 1001
        }
    )
    assert send_message1.status_code == 400

    send_message2 = requests.post(config.url + "message/send/v1",
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': ''
        }
    )
    assert send_message2.status_code == 400


# Access error when channel_id is valid and the authorised user 
# is not a member of the channel

def test_message_send_unauthorised_user(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user2_token,
            'channel_id': channel1_id,
            'message': 'a' * 1001
        }
    )
    assert send_message1.status_code == 403


##### Implementation #####

# Valid Case
def test_message_send_valid(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello there'
        }
    )
    assert send_message1.status_code == 200


    




