import pytest
import requests
import json
from src import config

##########################################
########### auth_register tests ##########
##########################################

# Input error for invalid email
def test_reg_invalid_email_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    assert resp1.status_code == 400
    assert resp2.status_code == 400

# Input error for duplicate email
def test_reg_duplicate_email_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'john',
        'name_last': 'doe'
    }) 

    if resp1 == resp2:
        assert resp2.status_code == 400

# Input error for invalid password
def test_reg_invalid_password_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': '12345',
        'name_first': 'anna',
        'name_last': 'park'
    }) 
    assert resp1.status_code == 400 

# Input error for invalid name
def test_reg_invalid_name_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'a' * 53,
        'name_last': 'park'
    }) 
    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'a' * 53
    }) 
    assert resp1.status_code == 400 
    assert resp2.status_code == 400 

##### Implementation #####

# Assert correct return values for auth/register/v2
def test_reg_return_values_h():
    requests.delete(config.url + "clear/v1", json={})
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 
    
    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'email@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 

    token1 = json.loads(resp1.text)['token']
    id1 = json.loads(resp1.text)['auth_user_id']
    token2 = json.loads(resp2.text)['token']
    id2 = json.loads(resp2.text)['auth_user_id']

    assert json.loads(resp1.text) == {'token': token1, 'auth_user_id': id1}
    assert json.loads(resp2.text) == {'token': token2, 'auth_user_id': id2}
    assert id1 != id2
    assert resp1.status_code == 200
    assert resp2.status_code == 200

def test_reg_handle_h():
    requests.delete(config.url + "clear/v1", json={})
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 

    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'annabelle',
        'name_last': 'parkerparker'
    })

    token1 = json.loads(resp1.text)['token']
    token2 = json.loads(resp2.text)['token']

    profile1 = requests.get(config.url + "users/all/v1", params ={
        'token': token1
    })
    profile2 = requests.get(config.url + "users/all/v1", params ={
        'token': token2
    })  

    handle1 = json.loads(profile1.text)['users'][0]['handle_str']
    assert handle1 == 'annapark'

    handle2 = json.loads(profile2.text)['users'][1]['handle_str']
    assert handle2 == 'annabelleparkerparke'


##########################################
############ auth_login tests ############
##########################################

def test_login_email_not_belong_to_user():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    resp2 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'def@gmail.dom',
        'password': 'password',
    })
    assert resp2.status_code == 400

def test__login_incorrect_password():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    resp2 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'wrong password',
    })
    assert resp2.status_code == 400

##########################################
############ auth_logout tests ###########
##########################################

# Access error: invalid token
def test_logout_invalid_token():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    token = json.loads(user.text)['token']

    logout = requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    assert logout.status_code == 200

    logout1 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    assert logout1.status_code == 403

def test_logout():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    token1 = json.loads(register.text)['token']

    login1 = requests.post(config.url + "auth/login/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
    })
    token2 = json.loads(login1.text)['token']

    login2 = requests.post(config.url + "auth/login/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
    })
    token3 = json.loads(login2.text)['token']

    logout1 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    assert logout1.status_code == 200

    logout2 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token3
    })
    assert logout2.status_code == 200

    logout3 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token2
    })
    assert logout3.status_code == 200
