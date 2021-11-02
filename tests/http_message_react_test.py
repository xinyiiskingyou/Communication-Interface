import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
######### message/react/v1 tests #########
##########################################

# Access Error: invalid token
def test_react_invalid_token_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']
    message1_id = user1_channel_message_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert react.status_code == ACCESSERROR

# Access Error: invalid token
def test_react_invalid_token_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']
    message1_id = user1_send_dm
    
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert react.status_code == ACCESSERROR

# Input error: message_id is not valid 
def test_react_invalid_message_id(global_owner):
    user1_token = global_owner['token']

    # negative message_id
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': -1,
        'react_id': 1
    })
    assert react.status_code == INPUTERROR
    
    # message_id does not exist
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': 256,
        'react_id': 1
    })
    assert react.status_code == INPUTERROR

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': -1,
        'react_id': 1
    })
    assert react.status_code == ACCESSERROR

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': 256,
        'react_id': 1
    })
    assert react.status_code == ACCESSERROR

# Input error: react a message that has been removed
def test_react_invalid_message_id1(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']

    remove_message = requests.delete(config.url + "message/remove/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert remove_message.status_code == VALID

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == INPUTERROR

# Input error: react_id is not a valid react ID in channel
def test_react_invalid_react_id_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']

    # negative react_id
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': -1
    })
    assert react.status_code == INPUTERROR

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 256
    })
    assert react.status_code == INPUTERROR
    
    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': -1
    })
    assert react.status_code == ACCESSERROR

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 256
    })
    assert react.status_code == ACCESSERROR

# Input error: react_id is not a valid react ID in dm
def test_react_invalid_react_id_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']

    # negative react_id
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': -1
    })
    assert react.status_code == INPUTERROR

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 256
    })
    assert react.status_code == INPUTERROR
    
    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': -1
    })
    assert react.status_code == ACCESSERROR

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 256
    })
    assert react.status_code == ACCESSERROR

# Input error: the message already contains a react with ID react_id from in chanenl
def test_react_already_contain_react_id_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == INPUTERROR

    # Access Error: invalid token and message is already reacted
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == ACCESSERROR

# Input error: the message already contains a react with ID react_id in dm
def test_react_already_contain_react_id_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert react.status_code == VALID

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert react.status_code == INPUTERROR

    # Access Error: invalid token and message is already reacted
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
        'react_id': 1
    })
    assert react.status_code == ACCESSERROR

##### Implementation #####

# Valid case in channel
def test_react_valid_channel(global_owner, user1_channel_message_id, create_channel):
    user1_token = global_owner['token']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    reaction = json.loads(messages.text)['messages'][0]['reacts'][0]['is_this_user_reacted']
    assert reaction == True

# Valid case: member in channel can also react
def test_react_valid_channel_member(global_owner, create_channel, user1_channel_message_id):

    user1_token = global_owner['token']

    # invite user2 to the channel
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcertgh@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user2_data = user2.json()
    user2_id = user2_data['auth_user_id']
    user2_token = user2_data['token']

    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user2_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    # there are 2 users react the same message
    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    reaction = json.loads(messages.text)['messages'][0]['reacts'][0]['u_ids']
    assert len(reaction) == 2

# Valid case in dm
def test_react_valid_dm(global_owner, create_dm):
    user1_token = global_owner['token']

    send_dm_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': create_dm['dm_id'],
        'message': 'hello'
    })
    assert send_dm_message.status_code == VALID
    dm_data = send_dm_message.json()['message_id']

    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': dm_data,
        'react_id': 1
    })
    assert react.status_code == VALID

    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': user1_token,
        'dm_id': create_dm['dm_id'], 
        'start': 0 
    })
    reaction = json.loads(message.text)['messages'][0]['reacts'][0]['is_this_user_reacted']
    assert reaction == True
