import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
############ dm_leave tests ##############
##########################################

# Access Error: Invalid token
def test_leave_invalid_token(create_dm, global_owner):
    dm_id1 = create_dm['dm_id']
    token = global_owner['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': dm_id1
    })  
    assert respo.status_code == ACCESSERROR

# Input Error: dm_id does not refer to a valid DM
def test_error_leave_dmid(global_owner): 
    
    token = global_owner['token']
    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': -1
    })  
    assert respo.status_code == INPUTERROR

    respo1 = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': ''
    })  
    assert respo1.status_code == INPUTERROR

    respo2 = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': 123
    })
    
    assert respo2.status_code == INPUTERROR 

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    # access error when invalid token and invalid dm_id
    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': -1
    })  
    assert respo.status_code == ACCESSERROR

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': ''
    })  
    assert respo.status_code == ACCESSERROR

# Access Error: dm_id is valid and the authorised user is not a member of the DM
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
    assert respo.status_code == ACCESSERROR

# Access Error: Valid dm but authorised user is not a member of that dm
def test_leave_invalid_dmid(global_owner, register_user3):
    
    user1_token = global_owner['token']
    user2_token = register_user3['token']

    # user 1 creates a dm
    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user1_token, 
        'u_ids': []
    })
    assert dm1.status_code == VALID
    dm_id1 = json.loads(dm1.text)['dm_id']

    respo1 = requests.post(config.url + "dm/leave/v1", json = { 
        'token': user2_token, 
        'dm_id': dm_id1
    })  
    assert respo1.status_code == ACCESSERROR
    
    # user2 creates a dm
    dm2 = requests.post(config.url + "dm/create/v1", json = { 
        'token': user2_token, 
        'u_ids': []
    })
    assert dm2.status_code == VALID
    dm_id2 = json.loads(dm2.text)['dm_id']

    assert dm_id1 != dm_id2

    respo = requests.post(config.url + "dm/leave/v1", json = { 
        'token': user1_token, 
        'dm_id': dm_id2
    })  
    assert respo.status_code == ACCESSERROR

##### Implementation #####

# Valid case: member leaves dm
def test_leave_http_valid(global_owner, register_user2): 

    token1 = global_owner['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token1, 
        'u_ids': [u_id2]
    })
    dm_id1 = json.loads(dm1.text)['dm_id']

    respo = requests.post(config.url + "dm/leave/v1",json = { 
        'token': token2, 
        'dm_id': dm_id1,
    })  
    assert respo.status_code == VALID

# Valid case: creator leaves dm
def test_leave_http_valid_owner(create_dm, global_owner):

    token = global_owner['token']
    dm_id = create_dm['dm_id']
    respo = requests.post(config.url + "dm/leave/v1",json = { 
        'token': token, 
        'dm_id': dm_id,
    })  
    assert respo.status_code == VALID

# Valid case: creator has left the DM and the remaining members can also leave DM
def test_leave_creator_left(create_dm, global_owner, register_user2, register_user3):
    dm_id = create_dm['dm_id']
    creator_token = global_owner['token']

    creator_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': creator_token, 
        'dm_id': dm_id,
    })  
    assert creator_leave.status_code == VALID

    
    id2_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': register_user2['token'], 
        'dm_id': dm_id,
    })  
    assert id2_leave.status_code == VALID

    id3_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': register_user3['token'], 
        'dm_id': dm_id,
    })  
    assert id3_leave.status_code == VALID
