import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
######## admin_user_remove tests #########
##########################################

# Access error: invalid token
def test_admin_invalid_token(global_owner, register_user2):

    # create an invalid token
    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    u_id = register_user2['auth_user_id']
    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': u_id
    })
    assert remove.status_code == ACCESSERROR

# Input error: u_id does not refer to a valid user
def test_admin_remove_invalid_u_id(global_owner, register_user2):

    token = global_owner['token']
    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': -1
    })
    remove1 = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': ''
    })
    assert remove.status_code == INPUTERROR
    assert remove1.status_code == INPUTERROR

    # access error: u_id is invalid and authorised user is not a global owner
    token2 = register_user2['token']
    remove2 = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token2,
        'u_id': -1
    })
    assert remove2.status_code == ACCESSERROR

    # access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    remove3 = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': -1
    })
    assert remove3.status_code == ACCESSERROR

# Input error: u_id refers to a user who is the only global owner
def test_admin_global_owner(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': u_id
    })
    assert remove.status_code == INPUTERROR

    # access error: invalid token and u_id is the only global owner
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    remove3 = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': u_id
    })
    assert remove3.status_code == ACCESSERROR

# Access error: the authorised user is not a global owner
def test_admin_remove_not_global_owner(global_owner, register_user2):

    user1_id = global_owner['auth_user_id']
    user2_token = register_user2['token']

    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': user2_token,
        'u_id': user1_id
    })
    assert remove.status_code == ACCESSERROR

##### Implementation #####
# remove stream member
def test_admin_remove_valid(global_owner, register_user2, create_channel):

    # user 1 creates a channel
    user1_token = global_owner['token']
    channel_id = create_channel['channel_id']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    # invites user2 to join user1's channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    # user 1 creates a dm 
    dm = requests.post(config.url + "dm/create/v1", json ={ 
        'token': user1_token,
        'u_ids': [user2_id]
    })
    dm_data = dm.json()
    dm_id = dm_data['dm_id']

    assert dm.status_code == VALID

    # user2 sends a message in the channel
    message = requests.post(config.url + "message/send/v1", json ={
        'token': user2_token,
        'channel_id': channel_id,
        'message': 'hello there'
    })
    assert message.status_code == VALID

    # user2 sends a message in dm
    send_dm = requests.post(config.url + "message/senddm/v1",json = {
        'token': user2_token,
        'dm_id': dm_id,
        'message': 'hi'
    })
    assert send_dm.status_code == VALID

    # now remove user2
    remove = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': user1_token,
        'u_id': user2_id
    })
    assert remove.status_code == VALID

    # id2 is removed from id1's channel
    channel_detail = requests.get(config.url + "channel/details/v2", params = {
        'token': user1_token,
        'channel_id': channel_id
    })
    assert len(json.loads(channel_detail.text)['all_members']) == 1

    # id2 is removed from id1's dm
    dm_detail = requests.get(config.url + "dm/details/v1", params = { 
        'token': user1_token,
        'dm_id': [dm_id]
    })
    assert len(json.loads(dm_detail.text)['members']) == 1

    # the contents of the messages will be replaced by 'Removed user'
    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel_id,
        'start': 0
    })
    channel_message = json.loads(messages.text)['messages'][0]['message']
    assert channel_message == 'Removed user'

    dm = requests.get(config.url + "dm/messages/v1", params ={ 
        'token': user1_token,
        'dm_id': dm_id, 
        'start': 0
    })
    dm_message = json.loads(dm.text)['messages'][0]['message']
    assert dm_message == 'Removed user'

    assert channel_message == dm_message
    
    # there are only 1 valid user in user/all now
    user_list = requests.get(config.url + "users/all/v1", params ={
        'token': user1_token
    })
    assert len(json.loads(user_list.text)) == 1

    # the profile of removed user is still retrievable
    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': user1_token,
        'u_id': user2_id
    })  

    # name_first should be 'Removed' and name_last should be 'user'.
    assert profile.status_code == VALID
    assert json.loads(profile.text)['user']['name_first'] == 'Removed'
    assert json.loads(profile.text)['user']['name_last'] == 'user'
    
    # user2's email and handle should be reusable.
    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    assert user3.status_code == VALID

# Streams owners can remove other Streams owners (including the original first owner)
def test_admin_remove_valid1(global_owner, create_channel, register_user2):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']
    channel_id = create_channel['channel_id']

    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # user 1 creates a dm 
    dm = requests.post(config.url + "dm/create/v1", json ={ 
        'token': token,
        'u_ids': [u_id2]
    })
    dm_data = dm.json()
    dm_id = dm_data['dm_id']

    dm_detail = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id': [dm_id]
    })
    original_dm_length = json.loads(dm_detail.text)['members']
    assert len(original_dm_length) == 2

    # promote user2 to be a new stream owner
    promote = requests.post(config.url + "admin/userpermission/change/v1", json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 1
    })
    assert promote.status_code == VALID

    # promotes user2 to be a channel owner
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert resp1.status_code == VALID

    # there will be 2 oweers in the channel
    channel_detail = requests.get(config.url + "channel/details/v2", params = {
        'token': token2,
        'channel_id': channel_id
    })
    original_owner_length = len(json.loads(channel_detail.text)['owner_members'])
    assert original_owner_length == 2
    original_member_length = len(json.loads(channel_detail.text)['owner_members'])
    assert original_member_length == 2

    # remove the original first owner
    demote = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': token2,
        'u_id': u_id
    })
    assert demote.status_code == VALID

    # only user2 left in the channel
    channel_detail = requests.get(config.url + "channel/details/v2", params = {
        'token': token2,
        'channel_id': channel_id
    })
    assert len(json.loads(channel_detail.text)['all_members']) == 1
    assert original_member_length != len(json.loads(channel_detail.text)['all_members'])
    assert len(json.loads(channel_detail.text)['owner_members']) == 1
    assert original_owner_length != len(json.loads(channel_detail.text)['owner_members'])

    # only user2 left in the dm
    dm_detail = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id': dm_id
    })
    assert len(json.loads(dm_detail.text)['members']) == 1
    assert original_dm_length != len(json.loads(dm_detail.text)['members'])

# test the case when creator of the leave the dm
# and the member is removed from dm
def test_admin_remove_valid_dm(global_owner, register_user2):
    
    token = global_owner['token']

    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # user 1 creates a dm 
    dm = requests.post(config.url + "dm/create/v1", json ={ 
        'token': token,
        'u_ids': [u_id2]
    })
    dm_data = dm.json()
    dm_id = dm_data['dm_id']

    # creator leaves the dm 
    creator_leave = requests.post(config.url + "dm/leave/v1",json = { 
        'token': token, 
        'dm_id': dm_id,
    })  
    assert creator_leave.status_code == VALID

    # now remove user 2
    remove = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': token,
        'u_id': u_id2
    })
    assert remove.status_code == VALID

    # no one can access the dm_detail
    dm_detail = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id': dm_id
    })
    assert dm_detail.status_code == ACCESSERROR

def test_admin_remove_dm_coverage(global_owner, register_user2):

    # user 1 creates a channel
    user1_token = global_owner['token']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    # user 1 creates a dm with user2
    dm = requests.post(config.url + "dm/create/v1", json ={ 
        'token': user1_token,
        'u_ids': [user2_id]
    })
    dm_data = dm.json()
    dm_id = dm_data['dm_id']

    assert dm.status_code == VALID

    # user2 sends a message in dm
    send_dm = requests.post(config.url + "message/senddm/v1",json = {
        'token': user2_token,
        'dm_id': dm_id,
        'message': 'user2'
    })
    assert send_dm.status_code == VALID

    send_dm2 = requests.post(config.url + "message/senddm/v1",json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': 'user1'
    })
    assert send_dm2.status_code == VALID

    messages1 = requests.get(config.url + "dm/messages/v1", params ={
        'token': user1_token,
        'dm_id': dm_id,
        'start': 0
    })
    assert json.loads(messages1.text)['messages'][0]['message'] == 'user1'

    # now remove user2
    remove = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': user1_token,
        'u_id': user2_id
    })
    assert remove.status_code == VALID

    messages2 = requests.get(config.url + "dm/messages/v1", params ={
        'token': user1_token,
        'dm_id': dm_id,
        'start': 0
    })
    assert json.loads(messages2.text)['messages'][1]['message'] == 'Removed user'
    
def test_admin_remove_channel_coverage(global_owner, register_user2, create_channel):
    # user 1 creates a channel
    user1_token = global_owner['token']
    channel_id = create_channel['channel_id']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    # invites user2 to join user1's channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    # user2 sends a message in the channel
    message = requests.post(config.url + "message/send/v1", json ={
        'token': user2_token,
        'channel_id': channel_id,
        'message': 'hello there'
    })
    assert message.status_code == VALID

    # user1 sends a message in the channel
    message = requests.post(config.url + "message/send/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'message': 'user1'
    })

    # the contents of the messages will be replaced by 'Removed user'
    messages1 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel_id,
        'start': 0
    })
    assert json.loads(messages1.text)['messages'][0]['message'] == 'user1'

    # now remove user2
    remove = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': user1_token,
        'u_id': user2_id
    })
    assert remove.status_code == VALID 

    messages2 = requests.get(config.url + "channel/messages/v2", params ={
        'token': user1_token,
        'channel_id': channel_id,
        'start': 0
    })
    assert json.loads(messages2.text)['messages'][1]['message'] == 'Removed user'
    