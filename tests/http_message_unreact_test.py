import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
######## message/unreact/v1 tests ########
##########################################

# Access error: invalid token in channel
def test_unreact_invalid_token_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']
    message1_id = user1_channel_message_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert unreact.status_code == ACCESSERROR

# Access error: invalid token in dm
def test_unreact_invalid_token_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert unreact.status_code == ACCESSERROR

# Input error: message_id is not valid 
def test_react_invalid_message_id(global_owner):
    user1_token = global_owner['token']

    # negative message_id
    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': -1,
        'react_id': 1
    })
    assert unreact.status_code == INPUTERROR
    
    # message_id does not exist
    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': 256,
        'react_id': 1
    })
    assert unreact.status_code == INPUTERROR

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': -1,
        'react_id': 1
    })
    assert unreact.status_code == ACCESSERROR

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': 256,
        'react_id': 1
    })
    assert unreact.status_code == ACCESSERROR

# Input error: unreact a message that has been removed
def test_unreact_invalid_message_id1(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']

    remove_message = requests.delete(config.url + "message/remove/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert remove_message.status_code == VALID

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert unreact.status_code == INPUTERROR

# Input error: react_id is not a valid react ID in channel
def test_unreact_invalid_react_id_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']

    # negative react_id
    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': -1
    })
    assert unreact.status_code == INPUTERROR

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 256
    })
    assert unreact.status_code == INPUTERROR
    
    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': -1
    })
    assert unreact.status_code == ACCESSERROR

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 256
    })
    assert unreact.status_code == ACCESSERROR

# Input error: react_id is not a valid react ID in dm
def test_unreact_invalid_react_id_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']

    # negative react_id
    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': -1
    })
    assert unreact.status_code == INPUTERROR

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 256
    })
    assert unreact.status_code == INPUTERROR
    
    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': -1
    })
    assert unreact.status_code == ACCESSERROR

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 256
    })
    assert unreact.status_code == ACCESSERROR

# Input error: the message does not contain a react with ID react_id 
# from the authorised user in channel
def test_unreact_no_react_id_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert unreact.status_code == INPUTERROR

    # Access Error: invalid token and the message is not reacted
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': -1
    })
    assert unreact.status_code == ACCESSERROR

# Input error: the message does not contain a react with ID react_id 
# from the authorised user in dm
def test_unreact_no_react_id_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert unreact.status_code == INPUTERROR

    # Access Error: invalid token and the message is not reacted
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert unreact.status_code == ACCESSERROR

##### Implementation #####

# valid case in channel
def test_unreact_valid_channel(global_owner, user1_channel_message_id, create_channel):
    user1_token = global_owner['token']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert unreact.status_code == VALID

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    reaction = json.loads(messages.text)['messages'][0]['reacts'][0]['is_this_user_reacted']
    assert reaction == False

# valid case in dm
def test_unreact_valid_dm(global_owner, create_dm, user1_send_dm):
    user1_token = global_owner['token']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert react.status_code == VALID

    unreact = requests.post(config.url + "message/unreact/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert unreact.status_code == VALID

    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': create_dm['dm_id'], 
        'start': 0 
    })
    reaction = json.loads(message.text)['messages'][0]['reacts'][0]['is_this_user_reacted']
    assert reaction == False
