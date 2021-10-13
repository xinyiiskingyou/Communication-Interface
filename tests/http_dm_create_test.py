import pytest
import requests
import json
from src import config 

##########################################
######### dm_create tests ##########
##########################################

# u_id empty
# one of u_ids not valid
def test_invalid_u_id():
    requests.delete(config.url + "clear/v1")
    creator = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(creator.text)['token']

    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abcertgh@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
        })

    u_id1 = json.loads(user1.text)['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': '1531camel@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'alast'
        })

    u_id2 = json.loads(user2.text)['auth_user_id']

    resp1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, -1]
        })
    assert resp1.status_code == 400

def test_valid_empty_u_id():
    requests.delete(config.url + "clear/v1")
    creator = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(creator.text)['token']

    resp1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': []
        })
    assert resp1.status_code == 200

def test_valid_u_ids():
    requests.delete(config.url + "clear/v1")
    creator = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(creator.text)['token']

    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abcertgh@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
        })

    u_id1 = json.loads(user1.text)['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': '123456@gmail.com',
            'password': 'password',
            'name_first': 'baby',
            'name_last': 'shark'
        })

    u_id2 = json.loads(user2.text)['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': '1531camel@gmail.com',
            'password': 'password',
            'name_first': 'alan',
            'name_last': 'wood'
        })

    u_id3 = json.loads(user3.text)['auth_user_id']
    resp1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, u_id3]
        })

    assert resp1.status_code == 200