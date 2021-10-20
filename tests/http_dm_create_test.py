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


# u_id empty
# one of u_ids not valid

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




