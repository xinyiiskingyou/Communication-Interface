import pytest
import requests
import json
from src import config
from src.other import clear_v1

##########################################
########## channel_details tests #########
##########################################

# Access error when token is not valid
def test_details_invalid_token():
    requests.delete(config.url + "clear/v1")
    # Register user and create channel
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']

    # token of a non-registered member
    token2 = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoX3VzZXJfaWQiOjJ9.jeXV_YsnPUUjY1Rjh3Sbzo4rw10xO0CUjuRV-JKqVYA'

    # Public
    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': True
    })

    resp1 = requests.get(config.url + "channel/details/v2", 
        params = {
            'token': token2,
            'channel_id': json.loads(channel1.text)['channel_id']
        })
    
    assert resp1.status_code == 403

    # Private
    channel2 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel2',
        'is_public': False
    }) 
    
    resp2 = requests.get(config.url + "channel/details/v2", 
        params = {
            'token': token2,
            'channel_id': json.loads(channel1.text)['channel_id']
        })
    
    assert resp2.status_code == 403


# Input error when channel_id is not valid
def test_details_invalid_channel_id_h():
    requests.delete(config.url + "clear/v1")
    # Register user and create channel
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': True
    })

    # Test invalid
    resp1 = requests.get(config.url + "channel/details/v2", 
        params = {
            'token': token1,
            'channel_id': -1
        })

    resp2 = requests.get(config.url + "channel/details/v2", 
        params = {
            'token': token1,
            'channel_id': 0
        })

    resp3 = requests.get(config.url + "channel/details/v2", 
        params = {
            'token': token1,
            'channel_id': 256
        })

    assert resp1.status_code == 400
    assert resp2.status_code == 400
    assert resp3.status_code == 400

# Access error when the person is not a member of the channel they want details from 
def test_deatils_not_member_h():
    requests.delete(config.url + "clear/v1")
    # Register user and create channel
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']

    # Public
    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': True
    })

    # Register another user
    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'email@gmail.com',
            'password': 'password',
            'name_first': 'john',
            'name_last': 'doe'
        })
    token2 = json.loads(user2.text)['token']
    
    # Test invalid 
    resp1 = requests.get(config.url + "channel/details/v2", 
        params = {
            'token': token2,
            'channel_id': json.loads(channel1.text)['channel_id']
        })
    
    assert resp1.status_code == 403


##### Implementation #####

# Check details for public channel
def test_details_return_values_pub_h():
    requests.delete(config.url + "clear/v1")

    # Register user and create channel
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': True
    })

    assert json.loads(channel1.text)['channel_id'] == 1
    # Get details of channel
    resp1 = requests.get(config.url + "channel/details/v2", 
        params = {
        'token': token1,
        'channel_id': json.loads(channel1.text)['channel_id'],
    })

    assert (json.loads(resp1.text) == 
        {
        'name': 'channel1',
        'is_public': True,
        'owner_members':[
            {
                'u_id': json.loads(channel1.text)['channel_id'],
                'email': 'abc@gmail.com',
                'name_first': 'anna',
                'name_last': 'park',
                'handle_str': 'annapark'
            }
        ],
        'all_members': [
            {
                'u_id': json.loads(channel1.text)['channel_id'],
                'email': 'abc@gmail.com',
                'name_first': 'anna',
                'name_last': 'park',
                'handle_str': 'annapark'
            }
        ]
    })

    assert resp1.status_code == 200


# Check details for private channel
def test_details_return_values_priv_h():
    requests.delete(config.url + "clear/v1")

    # Register user and create channel
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': False
    })

    channel_id1 = json.loads(channel1.text)['channel_id']
    assert channel_id1 > 0

    # Get details of channel
    resp1 = requests.get(config.url + "channel/details/v2", 
        params = {
        'token': token1,
        'channel_id': json.loads(channel1.text)['channel_id'],
    })

    assert (json.loads(resp1.text) == 
        {
        'name': 'channel1',
        'is_public': False,
        'owner_members':[
            {
                'u_id': json.loads(channel1.text)['channel_id'],
                'email': 'abc@gmail.com',
                'name_first': 'anna',
                'name_last': 'park',
                'handle_str': 'annapark'
            }
        ],
        'all_members': [
            {
                'u_id': json.loads(channel1.text)['channel_id'],
                'email': 'abc@gmail.com',
                'name_first': 'anna',
                'name_last': 'park',
                'handle_str': 'annapark'
            }
        ]
    })

    assert resp1.status_code == 200