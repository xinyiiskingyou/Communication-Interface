import pytest
import requests
import json
import smtplib
from src import config
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
#### auth_passwordreset_request tests ####
##########################################

def test_auth_passwordreset_request_valid():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'camel5363885.2@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    assert register.status_code == 200

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'camel5363885.2@gmail.com'
    })

    assert pass_request.status_code == 200

##########################################
##### auth_passwordreset_reset tests #####
##########################################

# Input Error: invalid code was given
def test_auth_passwordrequest_reset_invalid_code():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'camel5363885.2@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    assert register.status_code == 200

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'camel5363885.2@gmail.com'
    })

    assert pass_request.status_code == 200
    
    # Check invalid reset code
    pass_reset = requests.post(config.url + 'auth/passwordreset/reset/v1', json = {
        'reset_code': '',
        'new_password': 'new_password'
    })

    assert pass_reset.status_code == 400

# Input Error: password length is < 6 characters long
def test_auth_passwordrequest_reset_invalid_password_length():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    assert register.status_code == 200

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })
    assert pass_request.status_code == 200

    # Check invalid password length
    pass_reset = requests.post(config.url + 'auth/passwordreset/reset/v1', json = {
        'reset_code': 'resetcode',
        'new_password': '12345'
    })

    assert pass_reset.status_code == 400
    
