import pytest
import requests
import json
from src import config

@pytest.fixture
def register_user1():

    requests.delete(config.url + "clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    user1_data = user1.json()
    return user1_data

@pytest.fixture
def register_user2():

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'nani@gmail.com',
        'password': 'password',
        'name_first': 'john',
        'name_last': 'doe'
    })
    user2_data = user2.json()
    return user2_data

@pytest.fixture
def create_channel(register_user1):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user1['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data

##########################################
########## channel_join tests ############
##########################################

# Access error: invalid token
def test_join_invalid_token(register_user1, create_channel):

    token = register_user1['token']
    channel_id = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    join1 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': channel_id,
    })
    assert join1.status_code == 403


# Invalid channel_id 
def test_invalid_join_channel_id(register_user1):

    # Access error: invalid channel_id
    token = register_user1['token']
    join1 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': -16,
    })
    assert join1.status_code == 400

    join2 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': '',
    })
    assert join2.status_code == 400

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    join3 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': -16,
    })
    assert join3.status_code == 403

    join4 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': '',
    })
    assert join4.status_code == 403


# Input error: the authorised user is already a member of the public channel
def test_already_joined_public(register_user1, create_channel):

    token = register_user1['token']
    channel_id = create_channel['channel_id']

    channel_join_error = requests.post(config.url + 'channel/join/v2', json = { 
        'token': token,
        'channel_id' : channel_id
    })
    assert channel_join_error.status_code == 400

# Input error: the authorised user is already a member of the private channel
def test_already_joined_private(register_user1): 
    
    # create a user that has channel
    token = register_user1['token']

    private = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': False
    })
    channel_id = json.loads(private.text)['channel_id']

    channel_join_priv_error = requests.post(config.url + 'channel/join/v2', json = { 
        'token': token, 
        'channel_id': channel_id
    })
    assert channel_join_priv_error.status_code == 400

# AccessError when: channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
def test_join_priv_but_not_global_owner(register_user1, register_user2):

    # user 1 creates a private channel
    user1_token = register_user1['token']
    private = requests.post(config.url + "channels/create/v2", json = {
        'token': user1_token,
        'name': 'anna',
        'is_public': False
    })
    channel_id = json.loads(private.text)['channel_id']

    # user2 is not a channel member and not a global owner
    user2_token = register_user2['token']

    channel_join_priv_error = requests.post(config.url + 'channel/join/v2', json = { 
        'token': user2_token, 
        'channel_id': channel_id
    })
    assert channel_join_priv_error.status_code == 403

# valid case: the authorised user is able to join a public channel
def test_http_join(create_channel, register_user2): 

    channel_id1 = create_channel['channel_id']
    token2 = register_user2['token']

    respo1 = requests.post(config.url + "channel/join/v2", json = { 
        'token': token2, 
        'channel_id': channel_id1
    })
    assert respo1.status_code == 200
