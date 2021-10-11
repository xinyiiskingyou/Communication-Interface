import pytest
import requests
import json
from src import config 

##########################################
##### user_profile_set_email tests #######
##########################################

def test_user_set_email_invalid_email():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

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

def test_user_set_email_duplicate_email():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cat@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token1 = user1_data['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'elephant@gmail.com'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'cat@gmail.com'
    })
    assert mail.status_code == 400
    assert mail1.status_code == 400  

def test_user_set_email_valid():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cat@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })

    assert mail.status_code == 200

##########################################
##### user_profile_set_handle tests ######
##########################################
def test_user_set_handle_invalid_length():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a1'
    })

    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a' * 22
    })
    assert handle.status_code == 400
    assert handle1.status_code == 403

def test_user_set_handle_non_alphanumeric():
    
    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__++'
    })
    assert handle.status_code == 400

def test_user_set_handle_already_used():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token1 = user1_data['token']

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 200

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'anna'
    })
    assert handle.status_code == 400