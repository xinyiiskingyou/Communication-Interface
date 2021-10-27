import pytest
import requests
import json
from src import config

@pytest.fixture
def register_user1():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        'email': 'anna@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user2():
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'sallly@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    return user2_data

# user 1 cerates a channel
@pytest.fixture
def user1_channel_id(register_user1):
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': register_user1['token'],
        'name': 'anna_channel',
        'is_public': False
    })
    channel_data = channel.json()
    return channel_data['channel_id']

# user 1 sends a message in channel
@pytest.fixture
def user1_channel_message_id(register_user1, user1_channel_id):
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': register_user1['token'],
        'channel_id': user1_channel_id,
        'message': 'hello'
    })
    message1_id = json.loads(send_message1.text)['message_id']
    return message1_id

# user1 creates a dm with user2 
def user1_dm(register_user1, register_user2):
    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': register_user1['token'],
        'u_ids': [register_user2['auth_user_id']]
    })
    assert create_dm1.status_code == 200
    dm_id = json.loads(create_dm1.text)['dm_id']
    return dm_id

# user1 sends a message in dm
def user1_send_dm(register_user1, user1_dm):
    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': register_user1['token'],
        'dm_id': user1_dm,
        'message': 'hello'
    })
    assert send_dm1_message.status_code == 200
    dm_message_id = json.loads(send_dm1_message.text)['message_id']
    return dm_message_id

##########################################
########## message/pin/v1 tests ##########
##########################################

# Access error: invalid token in channel
def test_pin_invalid_token_channel(register_user1, user1_channel_message_id):
    user1_token = register_user1['token']
    message1_id = user1_channel_message_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
    })
    assert pin.status_code == 403

# Access error: invalid token in dm
def test_pin_invalid_token_dm(register_user1, user1_send_dm):
    user1_token = register_user1['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == 403

# Input error: message_id is not a valid message within a 
# channel or DM that the authorised user has joined
def test_pin_invalid_message_id(register_user1, register_user2, user1_channel_id):
    user1_token = register_user1['token']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': -1,
    })
    assert pin.status_code == 400

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': 256,
    })
    assert pin.status_code == 400

    # Access Error: invalid message_id and no owner permission
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': user1_channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == 200

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user2_token,
        'message_id': -1,
    })
    assert pin.status_code == 403

    # Access Error: invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': 256,
    })
    assert pin.status_code == 403

# Input error: pin a message that has been removed
# the message id is now invalid
def test_react_invalid_message_id1(register_user1, user1_channel_message_id):
    user1_token = register_user1['token']

    remove_message = requests.delete(config.url + "message/remove/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert remove_message.status_code == 200

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': -1,
    })
    assert pin.status_code == 400

# Input error: the message in channel is already pinned
def test_pin_already_pinned_channel(register_user1, user1_channel_message_id, user1_channel_id, register_user2):
    user1_token = register_user1['token']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == 200

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == 400

    # Access Error: message is already pinned and no owner permission
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user2_token,
        'channel_id': user1_channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == 200

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user2_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == 403

    # Access Error: invalid token and message is already pinned
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == 403

# Input error: the message in dm is already pinned
def test_pin_already_pinned_dm(register_user1, user1_send_dm):
    user1_token = register_user1['token']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == 200

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == 400

    # Access Error: invalid token and message is already pinned
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == 403

# Access Error: global owner is not a member of the channel and they are trying to 
# pin the message
def test_pin_global_owner_no_owner_permission_channel(register_user1, register_user2):
    user1_token = register_user1['token']

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
        'token': register_user1['token'],
        'channel_id': channel_id,
        'message': 'hello'
    })
    message_id = json.loads(send_message1.text)['message_id']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert pin.status_code == 403

# Access Error: channel member is trying to pin the message in the channel
def test_pin_member_no_owner_permission_channel(register_user1, register_user2, user1_channel_message_id, user1_channel_id):
    # user1 creates a channel
    user1_token = register_user1['token']

    # invite user2
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': user1_token,
        'channel_id': user1_channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == 200

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user2_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == 403

# Access Error: dm member is trying to pin the message in the dm
def test_pin_member_no_owner_permission_dm(register_user1, register_user2, user1_send_dm):

    user1_token = register_user1['token']
    user2_token = register_user2['token']
    assert user1_token != user2_token

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user2_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == 403

# Access Error: global owner is trying to pin the message in dm
def test_pin_global_owner_no_owner_permission_dm(register_user1, register_user2):
    
    user1_token = register_user1['token']
    user1_id = register_user1['auth_user_id']

    user2_token = register_user2['token']
    # user2 creates a dm with user1
    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user2_token,
        'u_ids': [user1_id]
    })
    assert create_dm1.status_code == 200
    dm_id = json.loads(create_dm1.text)['dm_id']

    # user1 sends a message in dm
    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm_id,
        'message': 'hello'
    })
    assert send_dm1_message.status_code == 200
    dm_message_id = json.loads(send_dm1_message.text)['message_id']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': dm_message_id,
    })
    assert pin.status_code == 403

##### Implementation #####

# valid case: channel owner can pin the message
def test_pin_channel_valid(register_user1, user1_channel_message_id, user1_channel_id):
    user1_token = register_user1['token']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_channel_message_id,
    })
    assert pin.status_code == 200

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': user1_channel_id,
        'start': 0
    })
    pinned = json.loads(messages.text)['messages'][0]['is_pinned']
    assert pinned == True

# valid case: global owner in a channel can pin the message
def test_pin_global_owner_channel_valid(register_user1, register_user2):

    user1_token = register_user1['token']
    user1_id = register_user1['auth_user_id']

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
    assert invite.status_code == 200

    # user2 sends a message
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': register_user1['token'],
        'channel_id': channel_id,
        'message': 'hello'
    })
    message_id = json.loads(send_message1.text)['message_id']

    # global owner in the channel can pin the message
    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': message_id,
    })
    assert pin.status_code == 200

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel_id,
        'start': 0
    })
    pinned = json.loads(messages.text)['messages'][0]['is_pinned']
    assert pinned == True

# valid case: owner of the dm can pin message
def test_pin_dm_valid(register_user1, user1_send_dm, user1_dm):

    user1_token = register_user1['token']

    pin = requests.post(config.url + "message/pin/v1", json = {
        'token': user1_token,
        'message_id': user1_send_dm,
    })
    assert pin.status_code == 200

    message = requests.get(config.url + "dm/messages/v1",params = { 
        'token': user1_token,
        'dm_id': user1_dm, 
        'start': 0 
    })
    pinned = json.loads(message.text)['messages'][0]['is_pinned']
    assert pinned == True
