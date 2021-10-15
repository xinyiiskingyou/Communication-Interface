import pytest
import requests
import json
from src import config

NUM_MESSAGE_EXACT = 50
NUM_MESSAGE_MORE = 100
NUM_MESSAGE_LESS = 25

@pytest.fixture
def setup():
    requests.delete(config.url + "clear/v1")


##############################################
########## channel/messages/v2 tests #########
##############################################

# Input error when channel_id does not refer to a valid channel
# Channel id is negative
def test_channel_messages_invalid_channel_id_negative(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    send_message = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': -1, 
            'start': 0
        }
    )
    assert send_message.status_code == 400


# Input Error when channel_id does not refer to a valid channel
# id is positive integer, but is not an id to any channel
def test_channel_messages_invalid_channel_id_nonexistant(setup):
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

    requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )

    requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user2_token,
            'name': 'sally_channel',
            'is_public': False
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': 256, 
            'start': 0
        }
    )
    assert messages.status_code == 400


# Input error when start is not a valid positive integer
# 1. Start is greater than total number of messages
# 2. Start is a negative number (< 0)
def test_channel_messages_invalid_start_gt(setup):
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

    messages1 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id, 
            'start': 256
        }
    )
    assert messages1.status_code == 400

    messages2 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id, 
            'start': -1
        }
    )
    assert messages2.status_code == 400


# Access error when channel_id is valid and the authorised user is not 
# a member of the channel
def test_channel_messages_unauthorised_user(setup):
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

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user2_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert messages.status_code == 403


##### Implementation #####

# Start index at most recent message (start = 0) and 
# does not return least recent message (i.e. num_messages > 50)
def test_channel_messages_start0__no_least_recent(setup):
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

    for i in range(NUM_MESSAGE_MORE):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == 50
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_EXACT

    assert messages.status_code == 200

# Start index at most recent message (start = 0) and 
# returns least recent message before end of pagination (i.e. num_messages < 50)
def test_channel_messages_start0__least_recent(setup):
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

    for i in range(NUM_MESSAGE_LESS):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_LESS

    assert messages.status_code == 200

# Start index at most recent message (start = 0) and 
# returns least recent message exactly at end of pagination (i.e. num_messages = 50)
def test_channel_messages_start0__least_recent_exactly(setup):
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

    for i in range(NUM_MESSAGE_EXACT):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_EXACT

    assert messages.status_code == 200

# Start index at neither most or least recent and 
# does not return least recent message 
def test_channel_messages_start_neither__no_least_recent(setup):
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

    for i in range(NUM_MESSAGE_MORE):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 10
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 10
    assert messages_end == 50 + 10
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_EXACT

    assert messages.status_code == 200

# Start index at neither most or least recent and 
# returns least recent message before end of pagination
def test_channel_messages_start_neither__least_recent(setup):
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

    for i in range(NUM_MESSAGE_LESS):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 10
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 10
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == 15

    assert messages.status_code == 200

# Start index at neither most or least recent and 
# returns least recent message exactly at end of pagination
def test_channel_messages_start_neither__least_recent_exactly(setup):
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

    for i in range(NUM_MESSAGE_EXACT + 10):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 10
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 10
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_EXACT

    assert messages.status_code == 200

# Start index at least recent
def test_channel_messages_start_least_recent(setup):
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

    for i in range(NUM_MESSAGE_EXACT):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 49
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 49
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == 1

    assert messages.status_code == 200

# No messages currently in channel
def test_channel_messages_empty(setup):
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

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == 0

    assert messages.status_code == 200