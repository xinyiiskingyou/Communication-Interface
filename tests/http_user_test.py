import pytest
import requests
import json
from src import config 

@pytest.fixture
def register_user1():
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
def register_user2():
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    return user2_data

##########################################
##### user_profile_set_email tests #######
##########################################

# Input Error when email entered is not a valid email
def test_user_set_email_invalid_email(register_user1):

    token = register_user1['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'abc'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': '123.com'
    })
    assert mail.status_code == 400
    assert mail1.status_code == 400

# email address is already being used by another user
def test_user_set_email_duplicate_email(register_user1, register_user2):

    user1_token = register_user1['token']
    user2_token = register_user2['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': user1_token,
        'email': 'elephant@gmail.com'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': user2_token,
        'email': 'cat@gmail.com'
    })
    assert mail.status_code == 400
    assert mail1.status_code == 400  

# valid case
def test_user_set_email_valid(register_user1):

    token = register_user1['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })

    assert mail.status_code == 200

##########################################
##### user_profile_set_handle tests ######
##########################################

# length of handle_str is not between 3 and 20 characters inclusive
def test_user_set_handle_invalid_length(register_user1):

    token = register_user1['token']

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a1'
    })

    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a' * 22
    })
    assert handle.status_code == 400
    assert handle1.status_code == 400

# handle_str contains characters that are not alphanumeric
def test_user_set_handle_non_alphanumeric(register_user1):
    
    token = register_user1['token']

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__++'
    })
    assert handle.status_code == 400

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__:  '
    })
    assert handle.status_code == 400

def test_user_set_handle(register_user1, register_user2):

    user1_token = register_user1['token']
    user2_token = register_user2['token']

    # valid case
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user1_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 200

    # the handle is already used by another user
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user2_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 400
