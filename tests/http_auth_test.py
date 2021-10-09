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
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    resp2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    assert resp1.status_code == 400
    assert resp2.status_code == 400

def test_reg_duplicate_email():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    resp2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail',
            'password': 'password',
            'name_first': 'john',
            'name_last': 'doe'
        }) 
              
    if resp1 == resp2:
        assert resp2.status_code == 400
        

def test_reg_invalid_password():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': '12345',
            'name_first': 'anna',
            'name_last': 'park'
        }) 
    
    assert resp1.status_code == 400 

def test_reg_invalid_name():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'a' * 53,
            'name_last': 'park'
        }) 
    resp2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'a' * 53
        }) 
    assert resp1.status_code == 400 
    assert resp2.status_code == 400 

###########################################################
############ Implementation for auth_register #############
###########################################################


