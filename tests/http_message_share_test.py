import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
######### message/share/v1 tests #########
##########################################

# Access error: invalid token in channel
def test_share_invalid_token_channel(global_owner, user1_channel_message_id, create_channel, create_dm):
    user1_token = global_owner['token']
    message1_id = user1_channel_message_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': 'hi', 
        'channel_id': create_channel['channel_id'],
        'dm_id': create_dm['dm_id']
    })
    assert share_message1.status_code == ACCESSERROR

###### Input Errors ######
# Both channel_id and dm_id are invalid 
def test_message_share_channel_and_dm_invalid(global_owner, create_channel, user1_channel_message_id):

    user1_token = global_owner['token']
    create_channel['channel_id']
    message1_id = user1_channel_message_id

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user1_token,
        'name': 'barry',
        'is_public': True
    })
    channel2.json()['channel_id']

    # channel_id is of valid type but is non-existant
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': 256,
        'dm_id': -1
    })
    assert share_message1.status_code == INPUTERROR

    # dm_id is of valid type but is non-existant
    share_message2 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': -1,
        'dm_id': 256
    })
    assert share_message2.status_code == INPUTERROR

    # Both channel_id and dm_id are negative values
    share_message3 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': -1,
        'dm_id': -1
    })
    assert share_message3.status_code == INPUTERROR

# Neither channel_id nor dm_id are -1 
def test_message_share_channel_and_dm_minus_1(global_owner, create_channel, 
user1_channel_message_id, create_dm):

    user1_token = global_owner['token']
    create_channel['channel_id']
    message1_id = user1_channel_message_id
    dm_id = create_dm['dm_id']

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user1_token,
        'name': 'barry',
        'is_public': True
    })
    channel2_id = channel2.json()['channel_id']

    # channel_id is of valid type but is non-existant
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': channel2_id,
        'dm_id': dm_id
    })
    assert share_message1.status_code == INPUTERROR

# og_message_id does not refer to a valid message within a channel/DM that the 
# authorised user has joined
    # 1. Not member of channel that og_message is in
def test_message_share_user_not_member_of_channel(global_owner, register_user2, create_channel, 
user1_channel_message_id):

    global_owner['token']
    user2_token = register_user2['token']
    create_channel['channel_id']

    message1_id = user1_channel_message_id

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': 'barry',
        'is_public': True
    })
    channel2_id = channel2.json()['channel_id']

    # User 2 is trying to share og_message from user1_channel which they are not part of
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user2_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': channel2_id,
        'dm_id': -1
    })
    assert share_message1.status_code == INPUTERROR

# og_message_id does not refer to a valid message within a channel/DM that the 
# authorised user has joined
    # 2. Not member of DM that og_message is in
def test_message_share_user_not_member_of_DM(global_owner, register_user2, register_user3, user1_send_dm):

    global_owner['token']
    user1_id = global_owner['auth_user_id']

    user2_token = register_user2['token']
    register_user2['auth_user_id']

    user3_token = register_user3['token']
    register_user3['auth_user_id']

    # User 2 creates a DM with User 1
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user2_token,
        'u_ids': [user1_id]
    })
    dm_id1 = dm1.json()['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': global_owner['token'],
        'dm_id': dm_id1,
        'message': 'hello'
    })
    assert send_dm1_message.status_code == VALID
    message1_id = json.loads(send_dm1_message.text)['message_id']

    # User 3 creates a DM with User 1
    dm2 = requests.post(config.url + "dm/create/v1", json = {
        'token': user3_token,
        'u_ids': [user1_id]
    })
    dm_id2 = dm2.json()['dm_id']

    # User 3 is trying to share og_message from dm_id1 which they are not part of 
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user3_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': -1,
        'dm_id': dm_id2
    })
    assert share_message1.status_code == INPUTERROR

# length of message is more than 1000 characters
def test_message_share_message_gt_1000_char(global_owner, create_channel, user1_channel_message_id):

    user1_token = global_owner['token']
    create_channel['channel_id']
    message1_id = user1_channel_message_id

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user1_token,
        'name': 'barry',
        'is_public': True
    })
    channel2_id = channel2.json()['channel_id']

    # channel_id is of valid type but is non-existant
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': 'a' * 1001, 
        'channel_id': channel2_id,
        'dm_id': -1
    })
    assert share_message1.status_code == INPUTERROR


###### Access Errors ######

# The pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid)
# and the authorised user has not joined the channel or DM they are trying to share the message to
    # 1. Not member of channel that message is being shared to
def test_message_share_message_not_member_of_channel_sharing_to(global_owner, register_user2, create_channel):

    global_owner['token']
    user2_token = register_user2['token']

    # User 1 (global owner) creates a channel
    create_channel = create_channel['channel_id']

    # User 2 creates a channel
    user2_channel = requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': 'barry',
        'is_public': True
    })
    user2_channel_id = user2_channel.json()['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': user2_channel_id,
        'message': 'hello'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user2_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': create_channel,
        'dm_id': -1
    })
    assert share_message1.status_code == ACCESSERROR

# The pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid)
# and the authorised user has not joined the channel or DM they are trying to share the message to
    # 2. Not member of DM that message is being shared to
def test_message_share_message_not_member_of_DM_sharing_to(global_owner, register_user2, register_user3):

    global_owner['token']
    user1_id = global_owner['auth_user_id']

    user2_token = register_user2['token']
    register_user2['auth_user_id']

    user3_token = register_user3['token']
    register_user3['auth_user_id']

    # User 2 creates a DM with User 1
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user2_token,
        'u_ids': [user1_id]
    })
    dm_id1 = dm1.json()['dm_id']

    # User 3 creates a DM with User 1
    dm2 = requests.post(config.url + "dm/create/v1", json = {
        'token': user3_token,
        'u_ids': [user1_id]
    })
    dm_id2 = dm2.json()['dm_id']

    # User 3 sends message in dm2
    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user3_token,
        'dm_id': dm_id2,
        'message': 'hello'
    })
    assert send_dm1_message.status_code == VALID
    message1_id = json.loads(send_dm1_message.text)['message_id']

    # User 3 is trying to share message from dm2 which are member of to dm1
    # which they are not member of 
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user3_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': -1,
        'dm_id': dm_id1
    })
    assert share_message1.status_code == ACCESSERROR


###### Implementation #######

# Share message from channel to channel
def test_message_share_channel_to_channel(global_owner, create_channel, user1_channel_message_id):

    user1_token = global_owner['token']
    create_channel['channel_id']
    message1_id = user1_channel_message_id

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user1_token,
        'name': 'barry',
        'is_public': True
    })
    channel2_id = channel2.json()['channel_id']

    # channel_id is of valid type but is non-existant
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': channel2_id,
        'dm_id': -1
    })
    message_share_id = share_message1.json()['shared_message_id']

    assert share_message1.status_code == VALID
    assert message1_id != message_share_id

# Share message from DM to DM
def test_message_share_DM_to_DM(global_owner, register_user2, register_user3):

    user1_token = global_owner['token']
    global_owner['auth_user_id']

    register_user2['token']
    user2_id = register_user2['auth_user_id']

    register_user3['token']
    user3_id = register_user3['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id]
    })
    dm1_id = create_dm1.json()['dm_id']
    
    create_dm2 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user3_id]
    })
    dm2_id = create_dm2.json()['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm1_id,
        'message': 'hello'
    })
    assert send_dm1_message.status_code == VALID
    message1_id = json.loads(send_dm1_message.text)['message_id']

    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': -1,
        'dm_id': dm2_id
    })
    assert share_message1.status_code == VALID

# Share message from DM to channel
def test_message_share_DM_to_channel(global_owner, register_user2, create_channel, 
create_dm, user1_send_dm):

    user1_token = global_owner['token']
    register_user2['token']

    channel1_id = create_channel['channel_id']
    create_dm['dm_id']

    message1_id = user1_send_dm

    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': '', 
        'channel_id': channel1_id,
        'dm_id': -1
    })
    assert share_message1.status_code == VALID

# Share message with additional message
def test_message_share_additional_message(global_owner, create_channel, user1_channel_message_id):

    user1_token = global_owner['token']
    create_channel['channel_id']
    message1_id = user1_channel_message_id

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user1_token,
        'name': 'barry',
        'is_public': True
    })
    channel2_id = channel2.json()['channel_id']

    # channel_id is of valid type but is non-existant
    share_message1 = requests.post(config.url + "message/share/v1", json ={
        'token': user1_token,
        'og_message_id': message1_id,
        'message': 'This is an additional message', 
        'channel_id': channel2_id,
        'dm_id': -1
    })
    assert share_message1.status_code == VALID
