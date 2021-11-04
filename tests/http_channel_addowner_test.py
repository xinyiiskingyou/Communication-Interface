import pytest
import requests
import json
from src import config 
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
######### channel_addowner tests #########
##########################################

# Access error: invalid token
def test_addowner_invalid_token(global_owner, register_user2, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']
    u_id = register_user2['auth_user_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == ACCESSERROR

# Input error: invalid channel_id
def test_invalid_channel_id(global_owner, register_user2):

    token = global_owner['token']
    u_id = register_user2['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 123,
        'u_id': u_id
    })

    resp2 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 'abc',
        'u_id': u_id
    })
    assert resp1.status_code == INPUTERROR
    assert resp2.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 123,
        'u_id': u_id
    })
    assert resp3.status_code == ACCESSERROR

 # Input error: invalid u_id
def test_invalid_u_id(global_owner, register_user2, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': -1
    })
    assert resp1.status_code == INPUTERROR

    # Access error: invalid u_id and token has no owner permission
    token2 = register_user2['token']
    u_id1 = register_user2['auth_user_id']

    # invite user2 to join the channel
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id1
    })
    
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': -1
    })

    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': 123
    })
    assert resp1.status_code == ACCESSERROR
    assert resp2.status_code == ACCESSERROR

    # Access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': -1
    })
    assert resp3.status_code == ACCESSERROR

# Input error: u_id not a member of the channel
def test_not_member_u_id(global_owner, register_user2, create_channel):

    # user1 creates a channel
    user1_token = global_owner['token']
    channel_id = create_channel['channel_id']

    # register user2 to not be a member of the channel
    user2_id = register_user2['auth_user_id']
    user2_token = register_user2['token']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp1.status_code == INPUTERROR

    # Access error: token has no owner permission and u_id is not a member
    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp2.status_code == ACCESSERROR 

    # Access error: invalid token and u_id is not a member of the channel
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp3.status_code == ACCESSERROR

# Input error: u_id refers to the user who is already owner of the channel
def test_already_owner(global_owner, register_user2, create_channel):

    # user1 creates a channel
    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']
    channel_id = create_channel['channel_id']

    # raise error as user1 is already the owner
    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })
    assert resp1.status_code == INPUTERROR

    # add user2 to be the owner of the channel
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp2.status_code == VALID

    # raise error since user2 is already the owner of the channel
    resp3 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp3.status_code == INPUTERROR

    # invite id3 to the channel
    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user3_token = json.loads(id3.text)['token']
    user3_id = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    # access error: token has no owner permission and u_id is already an owner
    resp4 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user3_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp4.status_code == ACCESSERROR

# Access error: channel_id is valid and the authorised user does not 
# have owner permissions in the channel
def test_no_perm_not_member(global_owner, register_user2, create_channel):

    # user 1 creates a channel
    user1_token = global_owner['token']
    channel_id = create_channel['channel_id']

    # invite user2 to the channel
    user2_id = register_user2['auth_user_id']
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })

    # register user3 to not be in the channel
    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user3_token = json.loads(id3.text)['token']

    # user3 is not able to add id2 to be the owner as user3 is not 
    # a member of the channel
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user3_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp1.status_code == ACCESSERROR

# more test for access error
def test_no_perm_not_owner(global_owner, create_channel, register_user2):

    # user1 creates a channel
    user1_token = global_owner['token']
    channel_id = create_channel['channel_id']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user3_id = json.loads(id3.text)['auth_user_id']

    # invite both user2 and user3 to the channel
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })

    # user2 is not able to add id3 to the channel 
    # as user2 does not have owener permission
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    assert resp1.status_code == ACCESSERROR

def test_global_owner_non_member_cant_addowner_private(global_owner, register_user2):
    global_owner_token = global_owner['token']

    channel_owner_token = register_user2['token']
    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': channel_owner_token,
        'name': 'anna',
        'is_public': False
    })
    channel_id = json.loads(channel.text)['channel_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'hellokitty@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'kitty'
    })
    user3_id = json.loads(id3.text)['auth_user_id']
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': channel_owner_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    # global owner is not able to add owener as they did not join the channel
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': global_owner_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    assert resp1.status_code == ACCESSERROR

def test_addowner_invalid_global(global_owner, register_user2):

    token = global_owner['token']

    # user 2 (not global owner) creates a channel
    token2 = register_user2['token']
    ch1 = requests.post(config.url + "channels/create/v2", json = {
        'token': token2,
        'name': '1531_CAMEl',
        'is_public': True
    })
    channel_id = json.loads(ch1.text)['channel_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'hellokitty@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'kitty'
    })
    u_id = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })

    # token1 cannot add id3 to be an owner 
    # since token1 is not in the channel
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == ACCESSERROR

##### Implementation ######

# valid case
def test_valid_addowner(global_owner, register_user2, create_channel):

    # user1 creates a channel
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    # register user2
    user2_id = register_user2['auth_user_id']
    
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': user2_id
    })

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': user2_id
    })

    assert resp1.status_code == VALID

# test valid case when global owner can add owner in the channel
def test_addowner_valid_global_private(global_owner, register_user2):

    token = global_owner['token']
    global_id = global_owner['auth_user_id']

    # user 2 (not global owner) creates a channel
    token2 = register_user2['token']
    ch1 = requests.post(config.url + "channels/create/v2", json = {
        'token': token2,
        'name': '1531_CAMEl',
        'is_public': False
    })
    channel_id = json.loads(ch1.text)['channel_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'hellokitty@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'kitty'
    })
    u_id = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': global_id
    })
    
    # token1 can add id3 to be an owner since token1 is a global owner
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == VALID
