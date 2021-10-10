import pytest
import requests
import json
from src import config
from src.other import clear_v1

##########################################
########## channel_details tests #########
##########################################

# Helper function to register a user
def register_user(email, password, name_first, name_last):
    return requests.post(config.url, 'auth/register/v2', {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

# Helper function to create a channel
def create_channel(token, name, is_public):
    return requests.post(config.url, 'channels/create/v2', {
        'token': token,
        'name': name,
        'is_public': is_public,
    })

# Helper function to invite someone to a channel
def invite_user(user1, channel_id, user2):
    return requests.post(config.url, 'channel/invite/v2', {
        'token': user1.get('token'),
        'channel_id': str(channel_id),
        'u_id': user2.get('u_id')
    })

def test_details_return_values():
    requests.delete(config.url + "clear/v1")

    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park'):
    channel1 = create_channel(user1.get('token'), 'channel_1', True)

    resp1 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': user1.get('token'),
            'channel_id': channel1.get('channel_id')
        })

    assert (json.loads(resp1.text) == 
        {
        'name': 'channel_1',
        'is_public': True,
        'owner_members':[
            {
                'u_id': 1,
                'email': 'abc@gmail.com',
                'name_first': 'anna',
                'name_last': 'park',
                'handle_str': 'annapark'
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'abc@gmail.com',
                'name_first': 'anna',
                'name_last': 'park',
                'handle_str': 'annapark'
            }
        ]
    })

    # Register another user and invite them to the channel
    user2 = register_user('abcd@gmail.com', 'password', 'john', 'doe'):
    invite_user(user1.get('token'), channel1.get('channel_id'), user1.get('token')

    # check all members
    assert details.get('all_members')[1]['auth_user_id'] == user2.get['auth_user_id']
    assert details.get('all_members')[1]['token'] == user2.get['token']

ef test_reg_invalid_email():
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

def test_channel_duplicate_email():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    resp2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
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
    print(resp1)
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