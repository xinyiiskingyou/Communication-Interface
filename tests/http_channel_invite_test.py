import pytest
import requests
import json
from src import config 
from tests.fixture import global_owner, register_user2, create_channel, register_user3
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########## channel_invite tests ##########
##########################################

# Access error: invalid token
def test_invite_invalid_token(global_owner, register_user2, create_channel):
    
    token = global_owner['token']
    u_id = register_user2['auth_user_id']
    channel = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': channel,
        'u_id': u_id
    })
    assert invite.status_code == ACCESSERROR

# Invalid u_id
def test_invite_invalid_u_id(global_owner, register_user2, create_channel):

    token = global_owner['token']
    channel = create_channel['channel_id']

    # Input Error: Invalid u_id
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': channel,
        'u_id': -16
    })
    assert invite.status_code == INPUTERROR

    # Access error:  when channel_id and the u_id are valid 
    #  but auth user is not a member of the channel
    user2_token = register_user2['token']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user2_token,
        'channel_id': channel,
        'u_id': -16
    })
    assert invite.status_code == ACCESSERROR

    # Access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': channel,
        'u_id': -16
    })
    assert invite.status_code == ACCESSERROR

# Invalid channel_id
def test_invite_invalid_channel_id(global_owner, register_user2):

    user_token = global_owner['token']
    u_id = register_user2['auth_user_id']

    # Input error: invalid channel_id
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user_token,
        'channel_id': -16,
        'u_id': u_id
    })
    assert invite.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user_token
    })
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user_token,
        'channel_id': -16,
        'u_id': u_id
    })
    assert invite.status_code == ACCESSERROR

# u_id is alreay a member of the channel    
def test_invite_already_member(global_owner, create_channel, register_user2, register_user3):

    # User1 is the channel_creator
    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']
    channel_id = create_channel['channel_id']

    # User2 and User3 do not belong to this channel
    user2_id = register_user2['auth_user_id']
    user3_token = register_user3['token']

    # Access error: valid channel_id but auth user is not a member of the channel 
    channel_invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user3_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert channel_invite.status_code == ACCESSERROR

    # Input Error: u_id refers to a user who is already a member of the channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })
    assert invite.status_code == INPUTERROR

    # Access error: invalid token and u_id is already a member of the channel
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })
    assert invite.status_code == ACCESSERROR

##### Implementation #####

# channel creator invites a user that is not a member of the channel
def test_valid_channel_invite(global_owner, create_channel, register_user2):

    token = global_owner['token']
    channel_id = create_channel['channel_id']
    u_id = register_user2['auth_user_id']

    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert invite.status_code == VALID
