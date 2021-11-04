import pytest
import requests
import json
from requests.api import request
from src import config 
from tests.fixture import global_owner, register_user2, register_user3, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
############ dm_details tests ############
##########################################

# invalid token
def test_http_dm_details_invalid_token(global_owner, create_dm):

    token = global_owner['token']
    dm_id = create_dm['dm_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert resp1.status_code == ACCESSERROR  

# invalid dm_id
def test_http_dm_details_invalid_dm_id(global_owner):

    token = global_owner['token']

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  -1
    })
    assert resp1.status_code == INPUTERROR

    # access error: invalid token and invalid dm_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  -1
    })
    assert resp1.status_code == ACCESSERROR

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
        'dm_id': dm_id
    })
    assert resp1.status_code == ACCESSERROR

def test_dm_details_not_valid(global_owner, register_user2): 

    token = global_owner['token']

    token1 = register_user2['token']
    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token,
        'u_ids': []
    })
    dm_id = json.loads(dm1.text)['dm_id']

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token1,
        'dm_id': dm_id
    })
    assert resp1.status_code == ACCESSERROR

def test_http_dm_details_valid(global_owner, register_user2): 

    token = global_owner['token']

    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token,
        'u_ids': [u_id2]
    })

    dm_id = json.loads(dm1.text)['dm_id']
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id':  dm_id
    })
    assert resp1.status_code == VALID 
