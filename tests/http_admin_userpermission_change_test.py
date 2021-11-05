import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
#### admin_userpermission_change tests ###
##########################################

# Access error: invalid token 
def test_admin_perm_invalid_token(global_owner, register_user2):
   
    token = global_owner['token']
    u_id = register_user2['auth_user_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id,
        'permission_id': 1
    })
    assert perm.status_code == ACCESSERROR

# Input error: u_id does not refer to a valid user
def test_admin_perm_invalid_u_id(global_owner, register_user2):

    token = global_owner['token']
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': -1,
        'permission_id': 1
    })
    assert perm.status_code == INPUTERROR

    perm1 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': '',
        'permission_id': 1
    })
    assert perm1.status_code == INPUTERROR

    # Access error: u_id is invalid the authorised user is not a global owner
    token2 = register_user2['token']
    perm2 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': -1,
        'permission_id': 1
    })
    assert perm2.status_code == ACCESSERROR

    # Access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    perm3 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': ' ',
        'permission_id': 1
    })
    assert perm3.status_code == ACCESSERROR

# Input error: u_id refers to a user who is the only global owner 
# and they are being demoted to a user
def test_admin_invalid_demote(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id,
        'permission_id': 2
    })
    assert perm.status_code == INPUTERROR

    # Access error: invalid token and demote the only owner
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    perm3 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id,
        'permission_id': 2
    })
    assert perm3.status_code == ACCESSERROR

# more case for the only global owner is being demoted
def test_admin_invalid_demote1(global_owner, register_user2):

    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    # user1 promotes user2
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': user1_token,
        'u_id': user2_id,
        'permission_id': 1
    })
    assert perm.status_code == VALID

    # id2 demotes id1
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': user2_token,
        'u_id': user1_id,
        'permission_id': 2
    })
    assert perm.status_code == VALID

    # raise Input error if user2 demotes themselves 
    # since user2 is now the only global owner
    perm2 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': user2_token,
        'u_id': user2_id,
        'permission_id': 2
    })
    assert perm2.status_code == INPUTERROR

# Input error: permission id is invalid 
def test_admin_invalid_permission_id(global_owner, register_user2):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 100
    })
    assert perm.status_code == INPUTERROR

    perm1 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': -100
    })
    assert perm1.status_code == INPUTERROR

    # Access error when permission id is invalid and the authorised user is not a global owner
    perm2 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 100
    })
    assert perm2.status_code == ACCESSERROR

    # Access error: invalid token and invalid permission id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    perm3 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': -1100
    })
    assert perm3.status_code == ACCESSERROR

# Access error: the authorised user is not a global owner
def test_admin_perm_not_global_owner(global_owner, register_user2):

    u_id = global_owner['auth_user_id']
    token2 = register_user2['token']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 1
    })
    assert perm.status_code == ACCESSERROR

# valid case
def test_valid_permission_change(global_owner, register_user2):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cute@unsw.edu.au',
        'password': 'password2',
        'name_first': 'tina',
        'name_last': 'huang'
    })
    user3_data = user3.json()
    token3 = user3_data['token']
    u_id3 = user3_data['auth_user_id']

    # id1 promotes id2 and id3
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 1
    })
    assert perm.status_code == VALID

    perm1 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id3,
        'permission_id': 1
    })
    assert perm1.status_code == VALID

    # now user3 has the permission to demote user1(the original owner)
    perm2 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token3,
        'u_id': u_id,
        'permission_id': 2
    })
    assert perm2.status_code == VALID

    # user2 also has the permission to promote user1 back
    perm3 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 1
    })
    assert perm3.status_code == VALID

# Nothing happened when the changing the permission is the same as before
def test_valid_permission_change1(global_owner, register_user2):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id,
        'permission_id': 1
    })
    assert perm.status_code == VALID

    u_id2 = register_user2['auth_user_id']
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 2
    })
    assert perm.status_code == VALID
