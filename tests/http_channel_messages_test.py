import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

NUM_MESSAGE_EXACT = 5
NUM_MESSAGE_MORE = 51
NUM_MESSAGE_LESS = 2
NUM_MESSAGE_END = 50
##############################################
########## channel/messages/v2 tests #########
##############################################

# Access error: invalid token 
def test_channel_messages_invalid_token(global_owner, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    send_message = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': channel_id, 
        'start': 0
    })
    assert send_message.status_code == ACCESSERROR

# Invalid channel_id
def test_channel_messages_invalid_channel_id_negative(global_owner):

    user1_token = global_owner['token']

    # Input error: invalid channel_id
    send_message = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': -1, 
        'start': 0
    })
    assert send_message.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    send_message = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': -1, 
        'start': 0
    })
    assert send_message.status_code == ACCESSERROR

# Invalid positive channel_id
def test_channel_messages_invalid_channel_id_nonexistant(global_owner, register_user2):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    requests.post(config.url + "channels/create/v2", json ={
        'token': user1_token,
        'name': 'anna_channel',
        'is_public': False
    })

    requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': 'sally_channel',
        'is_public': False
    })
    # Input Error: invalid channel_id
    # id is positive integer, but not refer to any valid channels
    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': 256, 
        'start': 0
    })
    assert messages.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    send_message = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': 256, 
        'start': 0
    })
    assert send_message.status_code == ACCESSERROR

# Invalid start
def test_channel_messages_invalid_start_gt(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    # Input error: invalid start 
    # start is greater than total number of messages
    messages1 = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id, 
        'start': 256
    })
    assert messages1.status_code == INPUTERROR

    # Input error: invalid start 
    # start is a negative number (< 0)
    messages2 = requests.get(config.url + "channel/messages/v2", params ={
            'token': user1_token,
            'channel_id': channel1_id, 
            'start': -1
    })
    assert messages2.status_code == INPUTERROR

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    
    # Access error: invalid token and invalid start number
    messages3 = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id, 
        'start': 256
    })
    assert messages3.status_code == ACCESSERROR

    # Access error: invalid token and invalid negative start number
    messages4 = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id, 
        'start': -1
    })
    assert messages4.status_code == ACCESSERROR

# Access error : valid channel_id and the authorised user is not 
# a member of the channel
def test_channel_messages_unauthorised_user(register_user2, create_channel):

    channel1_id = create_channel['channel_id']
    # user2 doesn't belong to this channel
    user2_token = register_user2['token']

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user2_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert messages.status_code == ACCESSERROR

    # user3 doesn't belong to this channel
    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'emily12234@gmail.com',
        'password': 'password',
        'name_first': 'emily',
        'name_last': 'wu'
    })
    user3_token = json.loads(user3.text)['token']
    messages1 = requests.get(config.url + "channel/messages/v2", params ={
        'token': user3_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert messages1.status_code == ACCESSERROR

##### Implementation #####

# Start index at most recent message (start = 0) and 
# does not return least recent message (i.e. num_messages > 50)
def test_channel_messages_start0__no_least_recent(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_MORE):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })
    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == NUM_MESSAGE_END
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_END

    assert messages.status_code == VALID

# Start index at most recent message (start = 0) and 
# returns least recent message before end of pagination (i.e. num_messages < 50)
def test_channel_messages_start0__least_recent(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_LESS):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_LESS

    assert messages.status_code == VALID

# Start index at most recent message (start = 0) and 
# returns least recent message exactly at end of pagination (i.e. num_messages = 50)
def test_channel_messages_start0__least_recent_exactly(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_EXACT):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_EXACT

    assert messages.status_code == VALID

# Start index at neither most or least recent and 
# does not return least recent message 
def test_channel_messages_start_neither__no_least_recent(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_MORE):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 1
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 1
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_END

    assert messages.status_code == VALID

# Start index at neither most or least recent and 
# returns least recent message before end of pagination
def test_channel_messages_start_neither__least_recent(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_LESS):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 1
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 1
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == 1

    assert messages.status_code == VALID

# Start index at neither most or least recent and 
# returns least recent message exactly at end of pagination
def test_channel_messages_start_neither__least_recent_exactly(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_EXACT + 10):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 10
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 10
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == NUM_MESSAGE_EXACT

    assert messages.status_code == VALID

# Start index at least recent
def test_channel_messages_start_least_recent(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    for i in range(NUM_MESSAGE_EXACT):
        requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': f'hi{i}'
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 4
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 4
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == 1

    assert messages.status_code == VALID

# No messages currently in channel
def test_channel_messages_empty(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })

    messages_start = json.loads(messages.text)['start']
    messages_end = json.loads(messages.text)['end']
    assert messages_start == 0
    assert messages_end == -1
    assert len(json.loads(messages.text)['messages']) == 0

    assert messages.status_code == VALID
