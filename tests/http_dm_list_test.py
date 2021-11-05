import pytest
import requests
import json
from src import config 
from tests.fixture import global_owner, register_user2, register_user3, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
############# dm_list tests ##############
##########################################

# Access Error: Invalid token
def test_dm_list_invalid_token(global_owner):
    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token,
    })
    assert resp1.status_code == ACCESSERROR

# Valid case: able to list the dms of 1 user who is ba part of one dm
def test_dm_list(global_owner, register_user2, register_user3):

    token = global_owner['token']

    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']
    token1 = register_user3['token']

    requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id2, u_id3]
    })

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token1,
    })

    assert resp1.status_code == VALID
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

# Valid case: empty list when no dm's have been created
def test_dm_list_no_dm(global_owner, register_user2, register_user3):

    token = global_owner['token']

    u_id2 = register_user2['auth_user_id']

    user3_token = register_user3['token']

    requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id2]
    })

    # user3 did not create any dm
    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': user3_token,
    })
    assert resp1.status_code == VALID
    assert json.loads(resp1.text) == {'dms': []}

# Valid case: able to list the dms of the user who created the dm
def test_dm_list_creator(global_owner, register_user2, register_user3):

    token = global_owner['token']
    
    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']

    requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id2, u_id3]
    })

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token,
    })
    assert resp1.status_code == VALID

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
