import pytest
import requests
import json
from src import config 
from tests.fixture import global_owner, register_user2, register_user3, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
############ dm_create tests #############
##########################################

# Access error: invalid token
def test_create_invalid_token(global_owner, register_user2):

    token = global_owner['token']
    user2_id = register_user2['auth_user_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [user2_id]
    })
    assert resp1.status_code == ACCESSERROR

# Input error: invalid u_id
def test_invalid_u_id(global_owner, register_user2):

    user1_token = global_owner['token']
    user2_id = register_user2['auth_user_id']

    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id, -1]
    })
    assert resp1.status_code == INPUTERROR

    # access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id, -1]
    })
    assert resp1.status_code == ACCESSERROR

# test no other members join dm
def test_valid_empty_u_id(global_owner):

    token = global_owner['token']
    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': []
    })
    assert resp1.status_code == VALID

# test members can join dm
def test_valid_u_ids(global_owner, register_user2, register_user3):

    token = global_owner['token']
    user1_id = global_owner['auth_user_id']

    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']

    resp1 = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [user1_id, u_id2, u_id3]
    })
    assert resp1.status_code == VALID
