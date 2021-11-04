import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
##### user_profile_set_handle tests ######
##########################################

# Access Error: invalid token
def test_user_set_handle_invalid_token(global_owner):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'ohno'
    })
    assert handle.status_code == ACCESSERROR

# Input error: length of handle_str is not between 3 and 20 characters inclusive
def test_user_set_handle_invalid_length(global_owner):

    token = global_owner['token']
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a1'
    })

    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a' * 22
    })
    assert handle.status_code == INPUTERROR
    assert handle1.status_code == INPUTERROR

    # Access Error: invalid token and invalid handle length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a1'
    })
    assert handle2.status_code == ACCESSERROR

    handle3 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a' * 22
    })
    assert handle3.status_code == ACCESSERROR

# Input error: handle_str contains characters that are not alphanumeric
def test_user_set_handle_non_alphanumeric(global_owner):
    
    token = global_owner['token']
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__++'
    })
    assert handle.status_code == INPUTERROR

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__:  '
    })
    assert handle.status_code == INPUTERROR

    # Access Error: invalid token and invalid characters
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '__ad31__++'
    })

    handle3 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': ' ___ad31__:'
    })
    assert handle2.status_code == ACCESSERROR
    assert handle3.status_code == ACCESSERROR

# valid case
def test_user_set_handle(global_owner, register_user2, create_dm, create_channel):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    
    channel_id = create_channel['channel_id']

    dm_id = create_dm['dm_id']
    
    # valid case
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user1_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == VALID

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': user1_token,
        'channel_id': channel_id
    })
    member_handle = json.loads(channel_details.text)['all_members'][0]['handle_str']
    assert member_handle == 'anna'
    owner_handle = json.loads(channel_details.text)['all_members'][0]['handle_str']
    assert owner_handle == member_handle

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': user1_token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['handle_str'] == 'anna'

    # the handle is already used by another user
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user2_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == INPUTERROR

# Change more then 2 users handle in a dm
def test_user_set_handle_dm_2_members(global_owner, register_user2):

    token1 = global_owner['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 cerates a dm with user 2
    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token1,
        'u_ids': [u_id2]
    })
    assert dm1.status_code == VALID

    # User 1 changes handle
    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'paiiiin'
    })
    assert handle1.status_code == VALID

    # User 2 changes handle
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token2,
        'handle_str': 'wwhyyyy'
    })
    assert handle2.status_code == VALID

# Make creator of dm leave and change creators name
def test_user_set_handle_valid_onwer_left(global_owner, create_dm):

    token1 = global_owner['token']

    # User 1 cerates a dm with user 2
    dm_id1 = create_dm['dm_id']

    # creator of dm leaves
    leave = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token1,
        'dm_id': dm_id1
    })
    assert leave.status_code == VALID

    # the creator of the dm who left changes handle
    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'paiin'
    })
    assert handle1.status_code == VALID

# Change more then 2 users handle in a channel
def test_user_set_handle_valid_channel_2_members(global_owner, register_user2, create_channel):

    token1 = global_owner['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 creates a channel with user 2
    channel_id1 = create_channel['channel_id']

    # user 1 invites user 2
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token1,
        'channel_id': channel_id1,
        'u_id': u_id2
    })
    assert invite.status_code == VALID

    # user 1 chnages email
    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'paiiin'
    })
    assert handle1.status_code == VALID
    
    # user 2 changes email
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token2,
        'handle_str': 'whyy'
    })
    assert handle2.status_code == VALID
