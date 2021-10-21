import pytest
import requests
import json
from src import config 

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

##########################################
############ dm_create tests #############
##########################################

# access error: invalid token
def test_create_invalid_u_id(creator, register_user1):

    invalid_token = creator['token'] + 'sdhakhfdskfds'
    user2_id = register_user1['auth_user_id']

    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': invalid_token,
        'u_ids': [user2_id]
    })
    assert resp1.status_code == 403

    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': '',
        'u_ids': [user2_id]
    })
    assert resp1.status_code == 403

# u_id empty
# one of u_ids not valid
def test_invalid_u_id(creator, register_user1):

    user1_token = creator['token']
    user2_id = register_user1['auth_user_id']

    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id, -1]
    })
    assert resp1.status_code == 400

    # access error: invalid token and invalid u_id
    invalid_token = creator['token'] + 'sdhakhfdskfds'
    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': invalid_token,
        'u_ids': [user2_id, -1]
    })
    assert resp1.status_code == 403

    resp2 = requests.post(config.url + "dm/create/v1", json = {
        'token': '',
        'u_ids': [user2_id, -1]
    })
    assert resp2.status_code == 403

# test no other members join dm
def test_valid_empty_u_id(creator):

    token = creator['token']
    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': []
    })
    assert resp1.status_code == 200

# test members can join dm
def test_valid_u_ids(creator, register_user1, register_user2, register_user3):

    token = creator['token']
    user1_id = register_user1['auth_user_id']

    u_id2 = register_user2['auth_user_id']

    u_id3 = register_user3['auth_user_id']

    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [user1_id, u_id2, u_id3]
    })

    assert resp1.status_code == 200

##########################################
############# dm_list tests ##############
##########################################

# access error: invalid token
def test_dm_list_invalid_token(creator):
    token = creator['token'] + 'sdaf'

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token,
    })
    assert resp1.status_code == 403

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': '',
    })
    assert resp1.status_code == 403

# valid case
def test_dm_list(creator, register_user1, register_user2, register_user3):

    token = creator['token']

    u_id1 = register_user1['auth_user_id']
    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']
    token1 = register_user3['token']

    requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id1, u_id2, u_id3]
    })

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token1,
    })

    assert resp1.status_code == 200
    dms = json.loads(resp1.text)['dms'][0]
    dm_id = dms['dm_id']
    name = dms['name']
    assert (json.loads(resp1.text) == 
        {
        'dms': [
            {
                'dm_id': dm_id,
                'name': name
            }
        ],
    })

def test_dm_list_no_dm(creator, register_user1, register_user2, register_user3):

    token = creator['token']

    u_id1 = register_user1['auth_user_id']
    u_id2 = register_user2['auth_user_id']

    user3_token = register_user3['token']

    requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id1, u_id2]
    })

    # user3 did not create any dm
    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': user3_token,
    })
    assert resp1.status_code == 200
    assert json.loads(resp1.text) == {'dms': []}

def test_dm_list_creator(creator, register_user1, register_user2, register_user3):

    token = creator['token']
    
    u_id1 = register_user1['auth_user_id']
    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']

    requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id1, u_id2, u_id3]
    })

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token,
    })
    assert resp1.status_code == 200

    dms = json.loads(resp1.text)['dms'][0]
    dm_id = dms['dm_id']
    name = dms['name']
    assert (json.loads(resp1.text) == 
        {
        'dms': [
            {
                'dm_id': dm_id,
                'name': name
            }
        ],
    })

##########################################
############# dm_remove tests ############
##########################################

# access error: invalid token
def test_dm_remove_invalid_token(creator, create_dm):

    token = creator['token'] + 'fsaddsf2'
    dm_id = create_dm['dm_id']
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp1.status_code == 403

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': '',
        'dm_id': dm_id
    })
    assert resp1.status_code == 403

# invalid dm_id
def test_dm_remove_invalid_dm_id(creator):

    token = creator['token']
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': -1
    })
    assert resp1.status_code == 400

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': ''
    })
    assert resp1.status_code == 400

    # access error: invalid token and invalid dm_id
    invalid_token = creator['token'] + 'fsaddsf2'
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': invalid_token,
        'dm_id': -1
    })
    assert resp1.status_code == 403

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': invalid_token,
        'dm_id': ''
    })
    assert resp1.status_code == 403

# dm_id is valid and the authorised user is not the original DM creator
def test_dm_remove_not_dm_creator(register_user3, create_dm):

    dm_id = create_dm['dm_id']
    token2 = register_user3['token']

    resp2 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token2,
        'dm_id': dm_id
    })
    assert resp2.status_code == 403

# access error when invalid dm_id and the token is not the original owner
def test_dm_remove_invalid_id_not_dm_creator(create_dm, register_user3):

    dm_id = create_dm['dm_id']
    assert dm_id != None

    token2 = register_user3['token']

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token2,
        'dm_id': -1
    })
    assert resp1.status_code == 400

# valid case
def test_dm_remove_valid(creator, create_dm):

    token = creator['token']
    dm_id = create_dm['dm_id']

    resp2 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp2.status_code == 200

##########################################
#########   Dm details tests    ##########
##########################################

# invalid token
def test_http_dm_details_invalid_token(creator, create_dm):

    invalid_token = creator['token'] +'sfhkjadhasd2'
    dm_id = create_dm['dm_id']
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': invalid_token,
        'dm_id':  dm_id
    })
    assert resp1.status_code == 403 

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': '',
        'dm_id':  dm_id
    })
    assert resp1.status_code == 403 

# invalid dm_id
def test_http_dm_details_invalid_dm_id(creator):

    token = creator['token']

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  -1
    })
    assert resp1.status_code == 400

    # access error: invalid token and invalid dm_id
    invalid_token = creator['token'] +'sfhkjadhasd2'
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': invalid_token,
        'dm_id':  -1
    })
    assert resp1.status_code == 403

# dm_id is valid and the authorised user is not a member of the DM
def test_http_dm_details_not_a_member(create_dm):

    dm_id = create_dm['dm_id']
    new_user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = new_user.json()
    token = user_data['token']

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert resp1.status_code == 403

def test_http_dm_details_valid(creator, register_user1): 

    token = creator['token']

    token2 = register_user1['token']
    u_id2 = register_user1['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token,
        'u_ids': [u_id2]
    })

    dm_id = json.loads(dm1.text)['dm_id']
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id':  dm_id
    })
    name = json.loads(resp1.text)['name']
    members = json.loads(resp1.text)['members']
    assert resp1.status_code == 200 
    assert (json.loads(resp1.text) == 
        {
        'name': name,
        'members': members
    })
##########################################
#########   Dm leave tests      ##########
##########################################

# invalid token
def test_leave_invalid_token(create_dm, register_user1):
    dm_id1 = create_dm['dm_id']
    invalid_token = register_user1['token'] +'agadsf'

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': invalid_token, 
        'dm_id': dm_id1
    })  
    assert respo.status_code == 403

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': '', 
        'dm_id': dm_id1
    })  
    assert respo.status_code == 403

# dm_id does not refer to a valid DM
def test_error_leave_dmid(creator): 
    
    token = creator['token']
    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': -1,
    })  
    assert respo.status_code == 400

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': '',
    })  
    assert respo.status_code == 400

    # access error when invalid token and invalid dm_id
    invalid_token = creator['token'] +'agadsf'
    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': invalid_token, 
        'dm_id': -1
    })  
    assert respo.status_code == 403

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': invalid_token, 
        'dm_id': ''
    })  
    assert respo.status_code == 403

# dm_id is valid and the authorised user is not a member of the DM
def test_dm_leave_not_a_member(create_dm):

    dm_id = create_dm['dm_id']
    new_user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = new_user.json()
    token = user_data['token']

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': dm_id
    })  
    assert respo.status_code == 403

# valid case: member leaves dm
def test_leave_http_valid(creator, register_user1): 

    token1 = creator['token']
    token2 = register_user1['token']
    u_id2 = register_user1['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token1, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']

    respo = requests.post(config.url + "dm/leave/v1",json = { 
        'token': token2, 
        'dm_id': dm_id1,
    })  
    assert respo.status_code == 200

# valid case: creator leaves dm
def test_leave_http_valid_owner(create_dm, creator):

    token = creator['token']
    dm_id = create_dm['dm_id']
    respo = requests.post(config.url + "dm/leave/v1",json = { 
        'token': token, 
        'dm_id': dm_id,
    })  
    assert respo.status_code == 200
    
##########################################
#########   Dm messages tests   ##########
##########################################

# invalid token
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

# dm_id does not refer to a valid DM
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

# start is greater than the total number of messages in the dm
# Input error when start is not a valid positive integer
# 1. Start is greater than total number of messages
# 2. Start is a negative number (< 0)
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


