import pytest
import requests
import json
from src import config
from src.other import clear_v1 


NUM_MESSAGE_EXACT = 50
NUM_MESSAGE_MORE = 100
NUM_MESSAGE_LESS = 25


@pytest.fixture
def creator():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'helloee@gmail.com',
        'password': 'password',
        'name_first': 'afirst',
        'name_last': 'alast'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user1():
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'emily12234@gmail.com',
        'password': 'password',
        'name_first': 'emily',
        'name_last': 'wu'
    })
    user1_data = user1.json()
    return user1_data

@pytest.fixture
def register_user2():
    user2 = requests.post(config.url + "auth/register/v2", json = {
        'email': '123456@gmail.com',
        'password': 'password',
        'name_first': 'baby',
        'name_last': 'shark'
    })
    user2_data = user2.json()
    return user2_data

@pytest.fixture
def register_user3():
    user3 = requests.post(config.url + "auth/register/v2", json = {
        'email': '1531camel@gmail.com',
        'password': 'password',
        'name_first': 'alan',
        'name_last': 'wood'
    })
    user3_data = user3.json()
    return user3_data

@pytest.fixture
def create_dm(creator, register_user1, register_user2, register_user3):
    token = creator['token']
    u_id1 = register_user1['auth_user_id']
    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id1, u_id2, u_id3]
    })
    dm_data = dm.json()
    return dm_data




def test_dm_messages_error_dm_id(creator, register_user1): 

    token = creator['token']
    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': token,
        'dm_id': -1, 
        'start': 0 
    })
    assert message.status_code == 400

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': token,
        'dm_id': -1,
        'message': 'hi'
    })
    assert resp.status_code == 400

    # invalid token and invalid dm_id
    invalid_token = register_user1['token'] +'agadsf'
    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': invalid_token,
        'dm_id': -1, 
        'start': 0 
    })
    assert message.status_code == 403

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': invalid_token,
        'dm_id': -1,
        'message': 'hi'
    })
    assert resp.status_code == 403


def test_dm_messages_invalid_start_gt(creator, create_dm):

    user1_token = creator['token']
    dm_id = create_dm['dm_id']

    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': user1_token,
        'dm_id': dm_id, 
        'start': 256
    })
    assert message.status_code == 400

    messages2 = requests.get(config.url + "dm/messages/v1", params ={
        'token': user1_token,
        'dm_id': dm_id, 
        'start': -1
    })
    assert messages2.status_code == 400

        # access error: invalid token and invalid start number
    invalid_token = creator['token'] + 'safadsfdsaf'
        
    messages3 = requests.get(config.url + "dm/messages/v1", params ={
        'token': invalid_token,
        'dm_id': dm_id, 
        'start': 256
    })
    assert messages3.status_code == 403

    messages4 = requests.get(config.url + "dm/messages/v1", params ={
        'token': invalid_token,
        'dm_id': dm_id, 
        'start': -1
    })
    assert messages4.status_code == 403

    
# dm_id is valid and the authorised user is not a member of the DM
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
    assert respo.status_code == 403

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': token,
        'dm_id': dm_id,
        'message': 'hi'
    })
    assert resp.status_code == 403

# valid case
def test_dm_message_valid_start0(creator, register_user1): 

    user1_token = creator['token']
    u_id2 = register_user1['auth_user_id']

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
    assert message_end == 50 
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_EXACT

    assert message.status_code == 200 

#check when server is back up 
def test_dm_message_valid_recent_exact(creator, register_user1): 

    user1_token = creator['token']
    u_id2 = register_user1['auth_user_id']

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
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 0 
    assert message_end == -1 
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_EXACT

    assert message.status_code == 200 

##check after server back up 
def test_dm_message_valid_no_recent(creator, register_user1): 

    user1_token = creator['token']
    u_id2 = register_user1['auth_user_id']

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
        'start': 10 
    })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 10 
    assert message_end == 50+10 
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_EXACT

    assert message.status_code == 200 


##check after server comes back on 
def test_dm_message_valid_neither(creator, register_user1): 

    user1_token = creator['token']
    u_id2 = register_user1['auth_user_id']

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
        'start': 10 
    })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 10 
    assert message_end == -1 
    assert len(json.loads(message.text)['messages']) == 15

    assert message.status_code == 200 

##empty 
def test_dm_message_valid_empty(creator, register_user1): 

    user1_token = creator['token']
    u_id2 = register_user1['auth_user_id']

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

    assert message.status_code == 200 




def test_messages_invalid_token(create_dm, creator):	
    dm_id1 = create_dm['dm_id']	
    invalid_token = creator['token'] +'agadsf'	
    message = requests.get(config.url + "dm/messages/v1", params = { 	
        'token': invalid_token,	
        'dm_id': dm_id1, 	
        'start': 0 	
    })	
    assert message.status_code == 403	
    resp = requests.post(config.url + "message/senddm/v1",json = {	
        'token': invalid_token,	
        'dm_id': dm_id1,	
        'message': 'hi'	
    })	
    assert resp.status_code == 403


# length of message is less than 1 or over 1000 characters
def test_message_send_dm_invalid_length(creator, create_dm, register_user1):

    user1_token = creator['token']
    dm_id = create_dm['dm_id']

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': ''
    })
    assert resp.status_code == 400

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': 'a' * 1001
    })
    assert resp.status_code == 400

    # invalid token and invalid length
    invalid_token = register_user1['token'] +'agadsf'
    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': invalid_token,
        'dm_id': dm_id,
        'message': 'a' * 1001
    })
    assert resp.status_code == 403

    resp = requests.post(config.url + "message/senddm/v1",json = {
        'token': invalid_token,
        'dm_id': dm_id,
        'message': ''
    })
    assert resp.status_code == 403
    

def test_notvalid_dm_id (): 	
    requests.delete(config.url + "clear/v1")	
    user = requests.post(config.url + "auth/register/v2", 	
        json = {	
            'email': 'abc@gmail.com',	
            'password': 'password',	
            'name_first': 'afirst',	
            'name_last': 'alast'	
        })	
    token = json.loads(user.text)['token']	
    resp1 = requests.get(config.url + "dm/messages/v1",	
        params = { 	
            'token': token,	
            'dm_id': -1,	
            'start': 0 	
        })	
    assert resp1.status_code == 400