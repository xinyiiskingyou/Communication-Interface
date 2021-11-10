import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel, create_dm, user1_send_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########## message/pin/v1 tests ##########
##########################################

# Access error: invalid token in channel
def test_unpin_invalid_token_channel(global_owner, user1_channel_message_id):
    user1_token = global_owner['token']
    message1_id = user1_channel_message_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
    })
    assert pin.status_code == ACCESSERROR

# Access error: invalid token in dm
def test_unpin_invalid_token_dm(global_owner, user1_send_dm):
    user1_token = global_owner['token']
    message1_id = user1_send_dm

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
    })
    assert pin.status_code == ACCESSERROR

def test_unpin_invalid_message_id_channel(global_owner, register_user2, create_channel):
    user1_token = global_owner['token']

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': -1,
    })
    assert pin.status_code == INPUTERROR

    # Input Error: invalid message_id and no owner permission
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    # user2 is invited as a member of the channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': -1,
    })
    assert pin.status_code == INPUTERROR

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': 256,
    })
    assert pin.status_code == ACCESSERROR

def test_unpin_invalid_message_id_dm(global_owner, register_user2):
    user1_token = global_owner['token']

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': -1,
    })
    assert pin.status_code == INPUTERROR

    # Input Error: invalid message_id and no owner permission
    # user2 is a member in dm
    user2_token = register_user2['token']

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': -1,
    })
    assert pin.status_code == INPUTERROR

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': 256,
    })
    assert pin.status_code == ACCESSERROR

# Input error: unpin a message that has been removed in channel
def test_unpin_removed_message_id1_channel(global_owner, user1_channel_message_id, register_user2, create_channel):
    user1_token = global_owner['token']

    remove_message = requests.delete(config.url + "message/remove/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert remove_message.status_code == VALID

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == INPUTERROR

    # Access Error: invalid message_id and no owner permission
    
    user2_id = register_user2['auth_user_id']

    # user2 is invited as a member to the channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    user2_token = register_user2['token']
    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == INPUTERROR

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == ACCESSERROR

# Input error: unpin a message that has been removed
def test_unpin_removed_message_id1_dm(global_owner, user1_send_dm, register_user2):
    user1_token = global_owner['token']

    remove_message = requests.delete(config.url + "message/remove/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert remove_message.status_code == VALID

    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == INPUTERROR

    # Access Error: invalid message_id and no owner permission
    # user2 is a member in dm
    user2_token = register_user2['token']
    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == INPUTERROR

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == ACCESSERROR

# The message in channel is not pinned
def test_unpin_not_pinned_channel(global_owner, user1_channel_message_id, create_channel, register_user2):
    user1_token = global_owner['token']

    # Input error: the message in channel is not pinned
    unpin1 = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert unpin1.status_code == INPUTERROR

    # Access Error: message is not pinned and no owner permission
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    unpin2 = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': user1_channel_message_id,
    })
    assert unpin2.status_code == ACCESSERROR

    # Access Error: invalid token and message is not pinned
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    unpin3 = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert unpin3.status_code == ACCESSERROR

# The message in dm is not pinned
def test_unpin_not_pinned_dm(global_owner, user1_send_dm, register_user2):
    user1_token = global_owner['token']

    # Input error: the message in dm is not pinned
    unpin1 = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert unpin1.status_code == INPUTERROR

    # Access Error: message is not pinned and no owner permission
    # user2 is a member in dm
    user2_token = register_user2['token']
    unpin2 = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': user1_send_dm,
    })
    assert unpin2.status_code == ACCESSERROR

    # Access Error: invalid token and message is not pinned
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    unpin3 = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert unpin3.status_code == ACCESSERROR

# Access Error: global owner has no owner permission to unpin a message
def test_pin_global_owner_no_owner_permission_channel(global_owner, register_user2):
    user1_token = global_owner['token']

    # user2 (not global owner) creates a channel
    user2_token = register_user2['token']
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': user2_token,
        'name': 'sally_channel',
        'is_public': True
    })
    channel_data = channel.json()
    channel_id = channel_data['channel_id']

    # user2 sends a message
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': register_user2['token'],
        'channel_id': channel_id,
        'message': 'hello'
    })
    message_id = json.loads(send_message1.text)['message_id']

    # user2 pins a message
    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user2_token,
        'message_id': message_id,
    })
    assert pin.status_code == VALID

    # user1 tries to unpin a message
    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert unpin.status_code == ACCESSERROR

# Access Error: channel member is trying to pin the message in the channel
def test_pin_member_no_owner_permission_channel(global_owner, register_user2, user1_channel_message_id, create_channel):
    # user1 creates a channel
    user1_token = global_owner['token']

    # invite user2
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'u_id': user2_id
    })
    assert invite.status_code == VALID

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == VALID

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': user1_channel_message_id,
    })
    assert unpin.status_code == ACCESSERROR

# Access Error: global owner is trying to pin the message in dm
def test_pin_global_owner_no_owner_permission_dm(global_owner, register_user2):
    
    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']

    user2_token = register_user2['token']
    # user2 creates a dm with user1
    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user2_token,
        'u_ids': [user1_id]
    })
    assert create_dm1.status_code == VALID
    dm_id = json.loads(create_dm1.text)['dm_id']

    # user2 sends a message in dm
    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm_id,
        'message': 'hello'
    })
    assert send_dm1_message.status_code == VALID
    dm_message_id = json.loads(send_dm1_message.text)['message_id']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user2_token,
        'message_id': dm_message_id,
    })
    assert pin.status_code == VALID

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': dm_message_id,
    })
    assert unpin.status_code == ACCESSERROR

# Access Error: dm member is trying to pin the message in the dm
def test_pin_member_no_owner_permission_dm(global_owner, register_user2, user1_send_dm):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    assert user1_token != user2_token

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == VALID

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user2_token,
        'message_id': user1_send_dm,
    })
    assert unpin.status_code == ACCESSERROR

##### Implementation #####

# valid case: channel owner can pin the message
def test_pin_channel_valid(global_owner, user1_channel_message_id, create_channel):
    user1_token = global_owner['token']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == VALID

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert unpin.status_code == VALID

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    pinned = json.loads(messages.text)['messages'][0]['is_pinned']
    assert pinned == False

# valid case: global owner in a channel can pin the message
def test_pin_global_owner_channel_valid(global_owner, register_user2):

    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']

    # user2 (not global owner) creates a channel
    user2_token = register_user2['token']
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': user2_token,
        'name': 'sally_channel',
        'is_public': True
    })
    channel_data = channel.json()
    channel_id = channel_data['channel_id']

    # user2 invites user1(global owner) to the channel
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })
    assert invite.status_code == VALID

    # user2 sends a message
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': global_owner['token'],
        'channel_id': channel_id,
        'message': 'hello'
    })
    message_id = json.loads(send_message1.text)['message_id']

    # global owner in the channel can pin the message
    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert pin.status_code == VALID

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert unpin.status_code == VALID

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel_id,
        'start': 0
    })
    pinned = json.loads(messages.text)['messages'][0]['is_pinned']
    assert pinned == False

# valid case: owner of the dm can pin message
def test_pin_dm_valid(global_owner, register_user2, create_dm):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    dm_id = create_dm['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm_id,
        'message': 'hello'
    })
    message_id = json.loads(send_dm1_message.text)['message_id']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert pin.status_code == VALID

    unpin = requests.post(config.url + "message/unpin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert unpin.status_code == VALID

    message = requests.get(config.url + "dm/messages/v1", params = { 
        'token': user1_token,
        'dm_id': dm_id, 
        'start': 0 
    })

    pinned = json.loads(message.text)['messages'][0]['is_pinned']
    assert pinned == False
