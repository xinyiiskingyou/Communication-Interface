import pytest
import requests
import json
from src import config 
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
###### channel_removeowner tests #########
##########################################

# access error: invalid token
def test_removeowner_invalid_token(global_owner, register_user2, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']
    user2_id = register_user2['auth_user_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert remove.status_code == ACCESSERROR

# invalid channel_id
def test_removeowner_invalid_channel_id(global_owner, register_user2):

    user_token = global_owner['token']
    user2_id = register_user2['auth_user_id']

    # invalid channel_id
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user_token,
        'channel_id': -1,
        'u_id': user2_id
    })
    assert remove.status_code == INPUTERROR

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user_token,
        'channel_id': -256,
        'u_id': user2_id
    })
    assert remove1.status_code == INPUTERROR

    # access error when invalid channel_id and invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user_token
    })
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user_token,
        'channel_id': -256,
        'u_id': user2_id
    })
    assert remove3.status_code == ACCESSERROR

# invalid u_id
def test_removeowner_invalid_u_id(global_owner, register_user2, create_channel):

    user1_token = global_owner['token']
    user1_channel = create_channel['channel_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': -16
    })
    assert remove.status_code == INPUTERROR
    #remove invalid 
    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': 'abc'
    })
    assert remove1.status_code == INPUTERROR

    # invite user2 to the the channel
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })

    # access error when invalid u_id and no owner permission
    remove2 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': -100
    })
    assert remove2.status_code == ACCESSERROR
    #remove invalid and not owner 
    remove4 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': 'abc'
    })
    assert remove4.status_code == ACCESSERROR

    # access error when invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': -16
    })
    assert remove3.status_code == ACCESSERROR

# u_id refers to a user who is not an owner of the channel
def test_removeowner_invalid_owner_u_id(global_owner, register_user2, create_channel):

    user1_token = global_owner['token']
    user1_channel = create_channel['channel_id']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    # invite user2 to the channel
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    # input error for u_id is not an owner
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove.status_code == INPUTERROR

    # access error when u_id is not an owner and token has no owner permission
    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove1.status_code == ACCESSERROR

    # access error when invalid token and u_id is not an owner
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove3.status_code == ACCESSERROR

# u_id refers to a user who is currently the only owner of the channel
def test_removeowner_only_owner(global_owner, register_user2, create_channel):

    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']
    user1_channel = create_channel['channel_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user1_id
    })
    assert remove.status_code == INPUTERROR

    # access error when u_id is the only owner and token has no owner permission
    user2_token = register_user2['token']
    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': user1_id
    })
    assert remove1.status_code == ACCESSERROR

    # access error when invalid token and u_id is not an owner
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    remove2 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user1_id
    })
    assert remove2.status_code == ACCESSERROR

# channel_id is valid and the authorised user does not have owner permissions in the channel
def test_removeowener_no_permission(global_owner, register_user2, create_channel, register_user3):

    user1_token = global_owner['token']
    user1_channel = create_channel['channel_id']

    user2_id = register_user2['auth_user_id']

    user3_id = register_user3['auth_user_id']
    user3_token = register_user3['token']

    # invite user1 and user2 to join the channel as a member
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user3_id
    })

    # add user2 to be an owner
    requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user3_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove.status_code == ACCESSERROR

def test_global_owner_nonmember_cannot_remove_owner(global_owner, register_user2, register_user3):
    global_owner_token = global_owner['token']

    channel_owner_token = register_user2['token']
    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': channel_owner_token,
        'name': 'anna',
        'is_public': True
    })
    channel_data = channel.json()
    channel_id = channel_data['channel_id']

    user3_id = register_user3['auth_user_id']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': channel_owner_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    assert invite.status_code == VALID

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': global_owner_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    assert remove.status_code == ACCESSERROR

# Global owner of streams that is member of channel is able to remove owners from channel
def test_remove_owner_global_owner(global_owner, register_user2, register_user3):
    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']
    user2_token = register_user2['token']

    user3_id = register_user3['auth_user_id']

    # User2 creates a channel
    user2_channel = requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': 'anna',
        'is_public': True
    })
    channel1_id = json.loads(user2_channel.text)['channel_id']

    # Invite user1 who is global owner of Streams
    invite1 = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user2_token,
        'channel_id': channel1_id,
        'u_id': user1_id
    })
    assert invite1.status_code == VALID

    # invite user3 to join the channel as a member
    invite3 = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user2_token,
        'channel_id': channel1_id,
        'u_id': user3_id
    })
    assert invite3.status_code == VALID

    # User2 (owner) adds User3 to be owner
    addowner3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user2_token,
        'channel_id': channel1_id,
        'u_id': user3_id
    })
    assert addowner3.status_code == VALID
    #remove global owner 
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': channel1_id,
        'u_id': user3_id
    })
    assert remove.status_code == VALID

# valid case
def test_remove_owner_valid(global_owner, register_user2, create_channel):

    user1_token = global_owner['token']
    user1_channel = create_channel['channel_id']

    user2_id = register_user2['auth_user_id']

    # invite user2 to join the channel as a member
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    # promote user2
    add = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert add.status_code == VALID

    # now it should have 2 owners in the channel
    details = requests.get(config.url + "channel/details/v2", params ={
        'token': user1_token,
        'channel_id': user1_channel
    })
    owner = json.loads(details.text)['owner_members']
    assert len(owner) == 2

    # remove id2
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove.status_code == VALID
    # only 1 owner in the channel
    details1 = requests.get(config.url + "channel/details/v2", params ={
        'token': user1_token,
        'channel_id': user1_channel
    })
    owner = json.loads(details1.text)['owner_members']
    assert len(owner) == 1
