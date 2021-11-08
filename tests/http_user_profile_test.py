import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########## user_profile tests ############
##########################################

# Access error when invalid token
def test_user_profile_invalid_token(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    profile1 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })
    assert profile1.status_code == ACCESSERROR

# Input error for invalid u_id
def test_user_profile_invalid_u_id(global_owner):

    token = global_owner['token']

    profile1 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': -1
    })

    profile2 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': 0
    })

    profile3 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': 256
    })

    assert profile1.status_code == INPUTERROR
    assert profile2.status_code == INPUTERROR
    assert profile3.status_code == INPUTERROR

    # Access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    profile4 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': -1
    })
    assert profile4.status_code == ACCESSERROR

##### Implementation #####

# Valid Case for looking at own profile
def test_user_profile_valid_own(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })

    assert profile.status_code == VALID
    assert (json.loads(profile.text)['user'] == 
        {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'lee',
        'handle_str': 'annalee',
        'profile_img_url': 'static/default_pic'
    })

# Valid Case for looking at someone else's profile
def test_user_profile_valid_someone_else(global_owner, register_user2):

    token = global_owner['token']
    u_id2 = (register_user2['auth_user_id'])

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id2
    })

    assert profile.status_code == VALID
    assert (json.loads(profile.text)['user'] == 
        {
        'u_id': u_id2,
        'email': 'elephant@gmail.com',
        'name_first': 'sally',
        'name_last': 'li',
        'handle_str': 'sallyli',
        'profile_img_url': 'static/default_pic'
    })