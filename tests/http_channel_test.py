import pytest
import requests
import json
from src import config
from src.other import clear_v1
from tests.server_tests_helper import register_user, create_channel, invite_user

##########################################
########## channel_details tests #########
##########################################

# Check details for public channel
def test_details_return_values_h():
    requests.delete(config.url + "clear/v1")

    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
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
    user2 = register_user('email@gmail.com', 'password', 'john', 'doe')
    invite_user(user1.get('token'), channel1.get('channel_id'), user2.get('token'))

    # check all members
    assert (resp1.get('all_members')[1]['auth_user_id'] == user2.get['auth_user_id'])
    assert (resp1.get('all_members')[1]['token'] == user2.get['token'])

# Check details for private channel
def test_details_return_values_priv_h():
    requests.delete(config.url + "clear/v1")

    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
    channel1 = create_channel(user1.get('token'), 'channel_1', False)

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
    user2 = register_user('email@gmail.com', 'password', 'john', 'doe')
    invite_user(user1.get('token'), channel1.get('channel_id'), user1.get('token'))

    # check all members
    assert details.get('all_members')[1]['auth_user_id'] == user2.get['auth_user_id']
    assert details.get('all_members')[1]['token'] == user2.get['token']

# Input error when channel_id is not valid
def test_details_invalid_channel_id_h():
    requests.delete(config.url + "clear/v1")
    # Register user 
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')

    # Test invalid
    resp1 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': user1.get('token'),
            'channel_id': -1
        })

    resp2 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': user1.get('token'),
            'channel_id': 0
        })

    resp3 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': user1.get('token'),
            'channel_id': 256
        })

    assert resp1.status_code == 400
    assert resp2.status_code == 400
    assert resp3.status_code == 400

# Access error when token is not valid
def test_details_invalid_token():
    requests.delete(config.url + "clear/v1")
    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
    channel1 = create_channel(user1.get('token'), 'channel_1', True) 

    # Test invalid 
    resp1 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': -1,
            'channel_id': user1.get('channel_id')
        })

    resp2 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': 'a',
            'channel_id': user1.get('channel_id')
        })

    resp3 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': 256,
            'channel_id': user1.get('channel_id')
        }) 
              
    assert resp1.status_code == 403
    assert resp2.status_code == 403
    assert resp3.status_code == 403
        
# WHen the person is not a member of the channel they want details from 
def test_deatils_not_member_h():
    requests.delete(config.url + "clear/v1")
     # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
    channel1 = create_channel(user1.get('token'), 'channel_1', True) 

    # Register another user
    user2 = register_user('email@gmail.com', 'password', 'john', 'doe')

    # Test invalid 
    resp1 = requests.post(config.url + "channel/details/v2", 
        json = {
            'token': user2.get('token'),
            'channel_id': user1.get('channel_id')
        })
    
    assert resp2.status_code == 403