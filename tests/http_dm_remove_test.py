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

def test_dm_remove_invalid_token(creator, create_dm):

    token = creator['token']
    dm_id = create_dm['dm_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
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
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': -1
    })
    assert resp1.status_code == 403

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': ''
    })
    assert resp1.status_code == 403

# dm_id is valid and the authorised user is not the original DM creator
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

# test after the creator left the dm and member cannot remove the dm
def test_leave_dm(creator, register_user1):
    
    # create a dm with user2
    creator_token = creator['token']
    user2_id = register_user1['auth_user_id']

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
    assert creator_leave.status_code == 200

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': creator_token,
        'dm_id': dm_id
    })
    assert resp1.status_code == 403

    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': creator_token,
        'dm_id': dm_id
    })
    assert resp1.status_code == 403

# valid case
def test_dm_remove_valid(creator, create_dm):

    token = creator['token']
    dm_id = create_dm['dm_id']

    resp2 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': dm_id
    })
    assert resp2.status_code == 200
    
