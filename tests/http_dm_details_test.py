import pytest
import requests
import json
from requests.api import request
from src import config 


@pytest.fixture
def global_owner():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cat@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    return user_data

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
############ dm_details tests ############
##########################################

# Access Error: invalid token
def test_http_dm_details_invalid_token(creator, create_dm):

    token = creator['token']
    dm_id = create_dm['dm_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert resp1.status_code == 403  

# Access Error: dm_id is valid and the authorised user is not a member of the DM
def test_dm_details_user_not_a_member(creator, register_user1): 

    token = creator['token']

    token1 = register_user1['token']

    dm1 = requests.post(config.url + "dm/create/v1",json = { 
        'token': token,
        'u_ids': []
    })
    dm_id = json.loads(dm1.text)['dm_id']

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token1,
        'dm_id': dm_id
    })
    assert resp1.status_code == 403

# Input Error: dm_id does not refer to a valid DM
def test_http_dm_details_invalid_dm_id(creator):

    token = creator['token']

    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  -1
    })
    assert resp1.status_code == 400

    # access error: invalid token and invalid dm_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
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

# valid case
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
    assert resp1.status_code == 200 
