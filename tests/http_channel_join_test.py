import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########## channel_join tests ############
##########################################

# Access error: invalid token
def test_join_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    join1 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': channel_id,
    })
    assert join1.status_code == ACCESSERROR

# Invalid channel_id 
def test_invalid_join_channel_id(global_owner):

    # Access error: invalid channel_id
    token = global_owner['token']
    join1 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': -16,
    })
    assert join1.status_code == INPUTERROR

    # Access error: invalid channel_id
    join2 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': '',
    })
    assert join2.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    join3 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': -16,
    })
    assert join3.status_code == ACCESSERROR

    # Access error: invalid token and invalid channel_id
    join4 = requests.post(config.url + 'channel/join/v2', json ={
        'token': token,
        'channel_id': '',
    })
    assert join4.status_code == ACCESSERROR

# Input error: the authorised user is already a member of the public channel
def test_already_joined_public(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    channel_join_error = requests.post(config.url + 'channel/join/v2', json = { 
        'token': token,
        'channel_id' : channel_id
    })
    assert channel_join_error.status_code == INPUTERROR

# Input error: the authorised user is already a member of the private channel
def test_already_joined_private(global_owner): 
    
    # this user is a private channel owner
    token = global_owner['token']

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
    assert channel_join_priv_error.status_code == INPUTERROR

# AccessError when: channel_id refers to a channel that is private 
# and the authorised user is neither a channel member nor a global owner
def test_join_priv_but_not_global_owner(global_owner, register_user2):

    # user1 is a private channel owner
    user1_token = global_owner['token']
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
    assert channel_join_priv_error.status_code == ACCESSERROR

##### Implementation #####

# valid case: the authorised user is able to join a public channel
def test_http_join(create_channel, register_user2): 

    channel_id1 = create_channel['channel_id']
    token2 = register_user2['token']

    respo1 = requests.post(config.url + "channel/join/v2", json = { 
        'token': token2, 
        'channel_id': channel_id1
    })
    assert respo1.status_code == VALID
