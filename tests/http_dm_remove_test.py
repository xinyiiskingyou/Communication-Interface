import pytest
import requests
import json
from src import config 
from tests.fixture import global_owner, register_user2, register_user3, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########### dm_remove tests ##############
##########################################

# Access Error: invalid token
def test_dm_remove_invalid_token(global_owner, create_dm):

    token = global_owner['token']
    dm_id = create_dm['dm_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp1.status_code == ACCESSERROR

# Input Error: invalid dm_id
def test_dm_remove_invalid_dm_id(global_owner):

    token = global_owner['token']
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': -1
    })
    assert resp1.status_code == INPUTERROR

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': ''
    })
    assert resp1.status_code == INPUTERROR

    # access error: invalid token and invalid dm_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': -1
    })
    assert resp1.status_code == ACCESSERROR

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': ''
    })
    assert resp1.status_code == ACCESSERROR

# Access Error: dm_id is valid and the authorised user is not the original DM creator
def test_dm_remove_not_dm_creator(create_dm):

    dm_id = create_dm['dm_id']
    user1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'anna@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user1_token = json.loads(user1.text)['token']

    resp2 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': user1_token,
        'dm_id': dm_id
    })
    assert resp2.status_code == ACCESSERROR

# Input Error: test after the creator left the dm and member cannot remove the dm
def test_leave_dm(global_owner, register_user2):
    
    # create a dm with user2
    creator_token = global_owner['token']
    user2_id = register_user2['auth_user_id']

    dm = requests.post(config.url + "dm/create/v1", json ={ 
        'token': creator_token,
        'u_ids': [user2_id]
    })
    dm_data = dm.json()
    dm_id = dm_data['dm_id']

    creator_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': creator_token, 
        'dm_id': dm_id,
    })  
    assert creator_leave.status_code == VALID

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': creator_token,
        'dm_id': dm_id
    })
    assert resp1.status_code == ACCESSERROR

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': creator_token,
        'dm_id': dm_id
    })
    assert resp1.status_code == ACCESSERROR

def test_dm_remove_twice(global_owner, create_dm):

    token = global_owner['token']
    dm_id = create_dm['dm_id']

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp1.status_code == VALID

    resp2 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp2.status_code == INPUTERROR

# Valid case: able to remove dm
def test_dm_remove_valid(global_owner, create_dm):

    token = global_owner['token']
    dm_id = create_dm['dm_id']

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp1.status_code == VALID
    assert resp1.json() == {}
    
    resp2 = requests.get(config.url + "dm/list/v1", params = {
        'token': token
    })
    assert resp2.status_code == VALID
    assert resp2.json() == {'dms': []}
