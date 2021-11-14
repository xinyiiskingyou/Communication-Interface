import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR
'''
NUM_MESSAGE_EXACT = 50
NUM_MESSAGE_MORE = 100
NUM_MESSAGE_LESS = 10
'''
NUM_MESSAGE_EXACT = 5
NUM_MESSAGE_MORE = 51
NUM_MESSAGE_LESS = 2
NUM_MESSAGE_END = 50
##########################################
### dm_messages & message_senddm tests ###
##########################################

# Access error: invalid token
def test_messages_invalid_token(create_dm, global_owner):	
    dm_id1 = create_dm['dm_id']	
    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    message = requests.get(config.url + "dm/messages/v1", params = { 	
        'token': token,	
        'dm_id': dm_id1, 	
        'start': 0 	
    })	
    assert message.status_code == ACCESSERROR	

    resp = requests.post(config.url + "message/senddm/v1",json = {	
        'token': token,	
        'dm_id': dm_id1,	
        'message': 'hi'	
    })	
    assert resp.status_code == ACCESSERROR

# Input error: dm_id does not refer to a valid DM
def test_dm_messages_error_dm_id(global_owner): 

    token = global_owner['token']
    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': token,
        'dm_id': -1, 
        'start': 0 
    })
    assert message.status_code == INPUTERROR

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': token,
        'dm_id': -1,
        'message': 'hi'
    })
    assert resp.status_code == INPUTERROR

    # invalid token and invalid dm_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': token,
        'dm_id': -1, 
        'start': 0 
    })
    assert message.status_code == ACCESSERROR

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': token,
        'dm_id': -1,
        'message': 'hi'
    })
    assert resp.status_code == ACCESSERROR

# Input error: start is greater than the total number of messages in the channel
def test_dm_messages_invalid_start_gt(global_owner, create_dm):

    user1_token = global_owner['token']
    dm_id = create_dm['dm_id']

    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': user1_token,
        'dm_id': dm_id, 
        'start': 256
    })
    assert message.status_code == INPUTERROR

    messages2 = requests.get(config.url + "dm/messages/v1", params ={
        'token': user1_token,
        'dm_id': dm_id, 
        'start': -1
    })
    assert messages2.status_code == INPUTERROR

    # access error: invalid token and invalid start number
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
        
    messages3 = requests.get(config.url + "dm/messages/v1", params ={
        'token': user1_token,
        'dm_id': dm_id, 
        'start': 256
    })
    assert messages3.status_code == ACCESSERROR

    messages4 = requests.get(config.url + "dm/messages/v1", params ={
        'token': user1_token,
        'dm_id': dm_id, 
        'start': -1
    })
    assert messages4.status_code == ACCESSERROR
    
# Access error: dm_id is valid and the authorised user is not a member of the DM
def test_dm_message_not_a_member(create_dm):

    dm_id = create_dm['dm_id']
    new_user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = new_user.json()
    token = user_data['token']

    respo = requests.get(config.url + "dm/messages/v1", params ={
        'token': token,
        'dm_id': dm_id, 
        'start': 0
    })
    assert respo.status_code == ACCESSERROR

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': token,
        'dm_id': dm_id,
        'message': 'hi'
    })
    assert resp.status_code == ACCESSERROR

# Input Error: length of message is less than 1 or over 1000 characters
def test_message_send_dm_invalid_length(global_owner, create_dm):

    user1_token = global_owner['token']
    dm_id = create_dm['dm_id']

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': ''
    })
    assert resp.status_code == INPUTERROR

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': 'a' * 1001
    })
    assert resp.status_code == INPUTERROR

    # invalid token and invalid length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': 'a' * 1001
    })
    assert resp.status_code == ACCESSERROR

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': ''
    })
    assert resp.status_code == ACCESSERROR

# Valid case: when start is 0
def test_dm_message_valid_start0(global_owner, register_user2): 

    user1_token = global_owner['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user1_token, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']

    for x in range(NUM_MESSAGE_MORE): 
        requests.post(config.url + "message/senddm/v1",
        json = {
            'token': user1_token,
            'dm_id': dm_id1,
            'message': f'hi{x}'
        })
    
    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': dm_id1, 
        'start': 0 
    })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 0 
    assert message_end == NUM_MESSAGE_END
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_END

    assert message.status_code == VALID 

# Valid case: sending 5 messages
def test_dm_message_valid_recent_exact(global_owner, register_user2): 

    user1_token = global_owner['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user1_token, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']

    for x in range(NUM_MESSAGE_EXACT): 
        requests.post(config.url + "message/senddm/v1",
        json = {
            'token': user1_token,
            'dm_id': dm_id1,
            'message': f'hi{x}'
        })
    
    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': dm_id1, 
        'start': 0 
    })
    assert message.status_code == VALID
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 0 
    assert message_end == -1 
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_EXACT
 
# Valid case: sending 8 messages
def test_dm_message_valid_no_recent(global_owner, register_user2): 

    user1_token = global_owner['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user1_token, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']

    for x in range(NUM_MESSAGE_MORE): 
        requests.post(config.url + "message/senddm/v1",
        json = {
            'token': user1_token,
            'dm_id': dm_id1,
            'message': f'hi{x}'
        })
    
    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': dm_id1, 
        'start': 1 
    })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 1
    assert message_end == -1 
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_END

    assert message.status_code == VALID 

# Valid case: sending 2 messages
def test_dm_message_valid_neither(global_owner, register_user2): 

    user1_token = global_owner['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user1_token, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']

    for x in range(NUM_MESSAGE_LESS): 
        requests.post(config.url + "message/senddm/v1",
        json = {
            'token': user1_token,
            'dm_id': dm_id1,
            'message': f'hi{x}'
        })
    
    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': dm_id1, 
        'start': 1 
    })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 1
    assert message_end == -1 
    assert len(json.loads(message.text)['messages']) == 1

    assert message.status_code == VALID 

# Valid case: no messages
def test_dm_message_valid_empty(global_owner, register_user2): 

    user1_token = global_owner['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user1_token, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']
    
    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': dm_id1, 
        'start': 0 
    })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 0 
    assert message_end == -1 
    assert len(json.loads(message.text)['messages']) == 0

    assert message.status_code == VALID 
