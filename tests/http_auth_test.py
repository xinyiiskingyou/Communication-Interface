import pytest
import requests
import json
from src import config
from src.other import clear_v1

##########################################
########### auth_register tests ##########
##########################################


def test_reg_invalid_email():
    clear_v1()
    resp1 = requests.get(config.url + 'email', params={'email': 'abc'})
    resp2 = requests.get(config.url + 'email', params={'email': 'abc@gmail'})
    assert(resp1.status_code == 400)
    assert(resp2.status_code == 400)

def test_reg_duplicate_email():
    clear_v1()
    resp1 = requests.get(config.url + 'email', params={'email': 'abc@gmail.com'})
    assert(resp1.status_code == 400)
    requests.get(config.url + 'email', params={'email': 'abc@gmail.com'})

def test_reg_invalid_password():
    clear_v1()
    resp1 = requests.get(config.url + 'email', params={'password': '12345'})
    assert(resp1.status_code == 400)

def test_reg_invalid_name():
    clear_v1()
    resp1 = requests.get(config.url + 'email', params={'name_first': 'a' * 50})
    resp2 = requests.get(config.url + 'email', params={'last_first': 'a' * 50})
    assert(resp1.status_code == 400)
    assert(resp2.status_code == 400)

###########################################################
############ Implementation for auth_register #############
###########################################################

def test_unique_token():
    clear_v1()
    resp1 = requests.get(config.url + 'auth/register/v2')
    resp1_data = resp1.json()

    resp2 = requests.get(config.url + 'auth/register/v2')
    resp2_data = resp2.json()

    assert resp1_data == {'token': '1', 'auth_user_id': 1}
    assert resp2_data == {'token': '2', 'auth_user_id': 2}
