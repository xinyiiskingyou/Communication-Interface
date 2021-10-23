import pytest
import requests
import json
from src import config

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
############ dm_leave tests ##############
##########################################

# Access Error: Invalid token
def test_leave_invalid_token(create_dm, register_user1):
    dm_id1 = create_dm['dm_id']
    token = register_user1['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': dm_id1
    })  
    assert respo.status_code == 403

# dm_id does not refer to a valid DM
def test_error_leave_dmid(creator): 
    
    token = creator['token']
    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': -1
    })  
    assert respo.status_code == 400

    respo1 = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': ''
    })  
    assert respo1.status_code == 400

    respo2 = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': 123
    })
    
    assert respo2.status_code == 400 

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    # access error when invalid token and invalid dm_id
    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': -1
    })  
    assert respo.status_code == 403

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
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

##### Implementation #####

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

# Creator has left the DM and the remaining members can also leave DM
def test_leave_creator_left(create_dm, creator, register_user1, register_user2, register_user3):
    dm_id = create_dm['dm_id']
    creator_token = creator['token']
    id1_token = register_user1['token']

    creator_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': creator_token, 
        'dm_id': dm_id,
    })  
    assert creator_leave.status_code == 200

    id1_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': id1_token, 
        'dm_id': dm_id,
    })  
    assert id1_leave.status_code == 200
    
    id2_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': register_user2['token'], 
        'dm_id': dm_id,
    })  
    assert id2_leave.status_code == 200

    id3_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': register_user3['token'], 
        'dm_id': dm_id,
    })  
    assert id3_leave.status_code == 200
