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

def test_dm_list_invalid_token(creator):
    token = creator['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "dm/list/v1", params = {
        'token': token,
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
