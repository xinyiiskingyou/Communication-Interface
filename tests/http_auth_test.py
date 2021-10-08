import pytest
import requests
import json
from src import config
from src.other import clear_v1

##########################################
########### auth_register tests ##########
##########################################
BASE_URL = 'http://127.0.0.1:8080'

def test_reg_invalid_email():
    clear_v1()
    resp1 = requests.post(config.url + 'register', data={'email': 'abc'})
    resp2 = requests.post(config.url + 'register', data={'email': 'abc@gmail'})
    assert(resp1.status_code == 400)
    assert(resp2.status_code == 400)

def test_reg_duplicate_email():
    clear_v1()
    resp1 = requests.post(config.url + 'register', data={'email': 'abc@gmail.com'})
    assert(resp1.status_code == 400)
    resp2 = requests.post(config.url + 'register', data={'email': 'abc@gmail.com'})

def test_reg_invalid_password():
    clear_v1()
    resp1 = requests.post(config.url + 'register', data={'password': '12345'})
    assert(resp1.status_code == 400)

def test_reg_invalid_name():
    clear_v1()
    resp1 = requests.post(config.url + 'register', data={'name_first': 'a' * 50})
    resp2 = requests.post(config.url + 'register', data={'last_first': 'a' * 50})
    assert(resp1.status_code == 400)
    assert(resp2.status_code == 400)

###########################################################
############ Implementation for auth_register #############
###########################################################


