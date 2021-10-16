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

##########################################
############# dm_list tests ##############
##########################################

def test_dm_list():
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
    token1 = json.loads(user3.text)['token']
    requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, u_id3]
        })

    resp1 = requests.get(config.url + "dm/list/v1", 
        params = {
            'token': token1,
        })
    assert resp1.status_code == 200
    assert (json.loads(resp1.text) == 
        {
        'dms': [
            {
                'dm_id': 1,
                'name': 'afirstalast, alanwood, babyshark, helloworld',
                'creator': {'u_id': 1, 'email': 'abc@gmail.com', 
                            'name_first': 'afirst', 'name_last': 'alast', 
                            'handle_str': 'afirstalast'},
                'members': [
                    {'u_id': 1, 'email': 'abc@gmail.com', 
                    'name_first': 'afirst', 'name_last': 'alast', 
                    'handle_str': 'afirstalast'},

                    {'u_id': 2, 'email': 'abcertgh@gmail.com', 
                    'name_first': 'hello', 'name_last': 'world', 
                    'handle_str': 'helloworld'},

                    {'u_id': 3, 'email': '123456@gmail.com', 
                    'name_first': 'baby', 'name_last': 'shark', 
                    'handle_str': 'babyshark'},

                    {'u_id': 4, 'email': '1531camel@gmail.com', 
                    'name_first': 'alan', 'name_last': 'wood', 
                    'handle_str': 'alanwood'}                    
                ],
                'messages': []
            }
        ],
    })

def test_dm_list_no_dm():
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


    user4 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': '1541camel@gmail.com',
            'password': 'password',
            'name_first': 'bob',
            'name_last': 'wood'
        })

    token2 = json.loads(user4.text)['token']

    requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, u_id3]
        })

    resp1 = requests.get(config.url + "dm/list/v1", 
        params = {
            'token': token2,
        })
    assert resp1.status_code == 200
    assert json.loads(resp1.text) == {'dms': []}

def test_dm_list_creator():
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

    requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, u_id3]
        })

    resp1 = requests.get(config.url + "dm/list/v1", 
        params = {
            'token': token,
        })
    assert resp1.status_code == 200
    assert (json.loads(resp1.text) == 
        {
        'dms': [
            {
                'dm_id': 1,
                'name': 'afirstalast, alanwood, babyshark, helloworld',
                'creator': {'u_id': 1, 'email': 'abc@gmail.com', 
                            'name_first': 'afirst', 'name_last': 'alast', 
                            'handle_str': 'afirstalast'},
                'members': [
                    {'u_id': 1, 'email': 'abc@gmail.com', 
                    'name_first': 'afirst', 'name_last': 'alast', 
                    'handle_str': 'afirstalast'},

                    {'u_id': 2, 'email': 'abcertgh@gmail.com', 
                    'name_first': 'hello', 'name_last': 'world', 
                    'handle_str': 'helloworld'},

                    {'u_id': 3, 'email': '123456@gmail.com', 
                    'name_first': 'baby', 'name_last': 'shark', 
                    'handle_str': 'babyshark'},

                    {'u_id': 4, 'email': '1531camel@gmail.com', 
                    'name_first': 'alan', 'name_last': 'wood', 
                    'handle_str': 'alanwood'}                    
                ],
                'messages': []
            }
        ],
    })

##########################################
############# dm_remove tests ############
##########################################

def test_dm_remove_invalid_dm_id():
    requests.delete(config.url + "clear/v1")
    creator = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(creator.text)['token']

    resp1 = requests.delete(config.url + "dm/remove/v1", 
        json = {
            'token': token,
            'dm_id': -1
        })
    assert resp1.status_code == 400

def test_dm_remove_not_dm_creator():
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
    token2 = json.loads(user3.text)['token']

    resp1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, u_id3]
        })
    dm_id = json.loads(resp1.text)['dm_id']

    resp2 = requests.delete(config.url + "dm/remove/v1", 
        json = {
            'token': token2,
            'dm_id': dm_id
        })
    assert resp2.status_code == 403

def test_dm_remove_invalid_id_not_dm_creator():
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
    token2 = json.loads(user3.text)['token']

    requests.post(config.url + "dm/create/v1", 
        json = {
            'token': token,
            'u_ids': [u_id1, u_id2, u_id3]
        })

    resp1 = requests.delete(config.url + "dm/remove/v1", 
        json = {
            'token': token2,
            'dm_id': -1
        })
    assert resp1.status_code == 400

def test_dm_remove_valid():
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
    dm_id = json.loads(resp1.text)['dm_id']

    resp2 = requests.delete(config.url + "dm/remove/v1", 
        json = {
            'token': token,
            'dm_id': dm_id
        })
    assert resp2.status_code == 200