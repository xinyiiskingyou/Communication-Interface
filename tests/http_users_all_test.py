import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
############ users_all tests #############
##########################################

# Access error when invalid token
def test_user_all_invalid_token(global_owner):
    token = global_owner['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    all1 = requests.get(config.url + "users/all/v1", params ={
        'token': token
    })
    assert all1.status_code == ACCESSERROR

# Valid case when there is only 1 user
def test_user_all_1_member(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']
    all1 = requests.get(config.url + "users/all/v1", params ={
        'token': token
    })
    assert all1.status_code == VALID

    assert (json.loads(all1.text)['users'] == 
    [{
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'lee',
        'handle_str': 'annalee',
        'profile_img_url': 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
    }])
    assert len(json.loads(all1.text)) == 1

# Valid case when there is more then 1 user
def test_user_all_several_members(global_owner, register_user2):

    token1 = global_owner['token']
    token2 = register_user2['token']

    all1 = requests.get(config.url + "users/all/v1", params ={
        'token': token1
    })

    all2 = requests.get(config.url + "users/all/v1", params ={
        'token': token2
    })

    # test using length of list as cannot be certain 
    # the listed order of users
    assert len(json.loads(all1.text)['users']) == 2
    assert len(json.loads(all2.text)['users']) == 2
    assert len(json.loads(all1.text)['users']) == len(json.loads(all2.text)['users'])
