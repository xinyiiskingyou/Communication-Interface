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
def test_details_return_values_pub_h():
    requests.delete(config.url + "clear/v1")

    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
    answer1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX3VzZXJfaWQiOjF9.csBzbal4Qczwb0lpZ8LzhpEdCpUbKgaaBV_bkYcriWw'
    channel1 = requests.post(config.url + "channels/create/v2", {
        'token': answer1,
        'name': 'channel1',
        'is_public': True
    })

    assert json.loads(channel1.text) == {'channel_id': 1}
    # Get details of channel
    resp1 = requests.get(config.url + "channel/details/v2", {
        'token': answer1,
        'channel_id': 1,
    })

    assert (json.loads(resp1.text) == 
        {
        'name': 'channel1',
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

# Input error when channel_id is not valid
def test_details_invalid_channel_id_h():
    requests.delete(config.url + "clear/v1")
    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
    answer1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX3VzZXJfaWQiOjF9.csBzbal4Qczwb0lpZ8LzhpEdCpUbKgaaBV_bkYcriWw'
    channel1 = requests.post(config.url + "channels/create/v2", {
        'token': answer1,
        'name': 'channel1',
        'is_public': True
    })

    # Test invalid
    resp1 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': answer1,
            'channel_id': -1
        })

    resp2 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': answer1,
            'channel_id': 0
        })

    resp3 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': answer1,
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
    answer1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX3VzZXJfaWQiOjF9.csBzbal4Qczwb0lpZ8LzhpEdCpUbKgaaBV_bkYcriWw'
    channel1 = requests.post(config.url + "channels/create/v2", {
        'token': answer1,
        'name': 'channel1',
        'is_public': True
    })

    # Test invalid 
    resp1 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': -1,
            'channel_id': 1
        })

    resp2 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': 'a',
            'channel_id': 1
        })

    resp3 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': 256,
            'channel_id': 1
        }) 
              
    assert resp1.status_code == 403
    assert resp2.status_code == 403
    assert resp3.status_code == 403
        
# WHen the person is not a member of the channel they want details from 
def test_deatils_not_member_h():
    requests.delete(config.url + "clear/v1")
    # Register user and create channel
    user1 = register_user('abc@gmail.com', 'password', 'anna', 'park')
    answer1 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX3VzZXJfaWQiOjF9.csBzbal4Qczwb0lpZ8LzhpEdCpUbKgaaBV_bkYcriWw'
    channel1 = requests.post(config.url + "channels/create/v2", {
        'token': answer1,
        'name': 'channel1',
        'is_public': True
    })

    # Register another user
    user2 = register_user('email@gmail.com', 'password', 'john', 'doe')
    answer2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX3VzZXJfaWQiOjJ9.jeXV_YsnPUUjY1Rjh3Sbzo4rw10xO0CUjuRV-JKqVYA'
    # Test invalid 
    resp1 = requests.get(config.url + "channel/details/v2", 
        json = {
            'token': answer2,
            'channel_id': 1
        })
    
    assert resp1.status_code == 403