import pytest
import requests
import json
from src import config 
from src.other import clear_v1

##########################################
######### channels_create tests ##########
##########################################

# AccessError Invalid auth_user_id
def test_create_invalid_auth_user_id():
    requests.delete(config.url + 'clear/v1')

    # Public
    resp1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': -16,
            'name': '1531_CAMEL',
            'is_public': True
        })


    resp2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 0,
            'name': '1531_CAMEL',
            'is_public': True
        })

    resp3 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 256,
            'name': '1531_CAMEL',
            'is_public': True
        })

    resp4 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 'not_an_id',
            'name': '1531_CAMEL',
            'is_public': True
        })

    resp5 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': '',
            'name': '1531_CAMEL',
            'is_public': True
        })

    # Input Error
    assert resp1.status_code == 400
    assert resp2.status_code == 400
    assert resp3.status_code == 400
    assert resp4.status_code == 400
    assert resp5.status_code == 400


    # Private
    resp6 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': -16,
            'name': '1531_CAMEL',
            'is_public': False
        })

    resp7 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 0,
            'name': '1531_CAMEL',
            'is_public': False
        })

    resp8 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 256,
            'name': '1531_CAMEL',
            'is_public': False
        })

    resp9 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 'not_an_id',
            'name': '1531_CAMEL',
            'is_public': False
        })

    resp10 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': '',
            'name': '1531_CAMEL',
            'is_public': False
        })

    assert resp6.status_code == 400
    assert resp7.status_code == 400
    assert resp8.status_code == 400
    assert resp9.status_code == 400
    assert resp10.status_code == 400

    # invalid auth_user_id with invalid channel name
    resp11 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': -16,
            'name': ' ',
            'is_public': False
        })

    resp12 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 1,
            'name': 'a' * 50,
            'is_public': True
        })

    resp13 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': 11,
            'name': '',
            'is_public': False
        })

    assert resp11.status_code == 400
    assert resp12.status_code == 400
    assert resp13.status_code == 400    


# InputError when length of name is less than 1 or more than 20 characters
def test_create_invalid_name():
    requests.delete(config.url + 'clear/v1')

    # Public
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    resp1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': '',
            'is_public': True
        })

    resp2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': '  ',
            'is_public': True
        })

    resp3 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': '                      ',
            'is_public': True
        })

    resp4 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': 'a' * 21,
            'is_public': True
        })


    resp5 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': 'a' * 50,
            'is_public': True
        })

    assert resp1.status_code == 400
    assert resp2.status_code == 400
    assert resp3.status_code == 400
    assert resp4.status_code == 400
    assert resp5.status_code == 400

##### Implementation #####
# Assert channel_id for one, two and three channels created by two different users
def test_create_valid_channel_id():
    requests.delete(config.url + 'clear/v1')

    # Public
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc1@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    resp1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': '1531_CAMEL_1',
            'is_public': True
        })

    assert resp1.status_code == 200

    resp2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id1['auth_user_id'],
            'name': '1531_CAMEL_2',
            'is_public': True
        })
    assert resp2.status_code == 200

    id2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc2@gmail.com',
            'password': 'password',
            'name_first': 'bfirst',
            'name_last': 'blast'
        })


    resp3 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id2['auth_user_id'],
            'name': '1531_CAMEL_3',
            'is_public': True
        })

    assert resp3.status_code == 200
    id3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc3@gmail.com',
            'password': 'password',
            'name_first': 'cfirst',
            'name_last': 'clast'
        })

    resp4 = requests.post(config.url + "channels/create/v2", 
        json = {
            'auth_user_id': id3['auth_user_id'],
            'name': '1531_CAMEL_3',
            'is_public': False
        })
    assert resp4.status_code == 200

'''
# Assert channel_id can never be a negative number
def test_create_negative_channel_id():
    requests.delete(config.url + 'clear/v1')
    auth_id = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v1(auth_id['auth_user_id'], '1531_CAMEL', True)
    assert channel_id1['channel_id'] > 0
'''