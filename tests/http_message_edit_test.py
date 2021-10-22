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

@pytest.fixture
def register_user2():
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    return user2_data

@pytest.fixture
def register_user3():
    user3 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'larry@gmail.com',
        'password': 'password',
        'name_first': 'larry',
        'name_last': 'li'
    })
    user3_data = user3.json()
    return user3_data

##########################################
########## message/edit/v1 tests #########
##########################################

# Test for invalid token
def test_channel_messages_invalid_token(register_user1, user1_channel_message_id):
    
    user1_token = register_user1['token']
    message1_id = user1_channel_message_id

    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': 'a' * 1001
    })
    assert edit_message.status_code == 403

# Input error when length of message is over 1000 characters
def test_message_edit_invalid_message_length(register_user1, register_user2, user1_channel_message_id):

    user1_token = register_user1['token']
    message1_id = user1_channel_message_id

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': 'a' * 1001
    })
    assert edit_message.status_code == 400

    user2_token = register_user2['token']
    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'message': 'a' * 1001
    })
    assert edit_message.status_code == 403

    # invalid token and invalid length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': 'a' * 1001
    })
    assert edit_message.status_code == 403

# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 1. Negative message_id
def test_message_edit_invalid_message_id_negative(register_user1):

    user1_token = register_user1['token']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': -1,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 400

    # invalid token and invalid message_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': -1,
        'message': 'heeeeloo'
    })
    assert edit_message.status_code == 403

# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 2. message_id is correct type (i.e. positive integer) but does not
    # exist with any message
def test_message_edit_invalid_message_id_nonexistant(register_user1):

    user1_token = register_user1['token']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': 256,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 400

    # invalid token
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': 256,
        'message': 'heeeeloo'
    })
    assert edit_message.status_code == 403

# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 3.a) message_id exists but does not belong to channel that user is part of
    # User has global permission of "Member"
def test_message_edit_invalid_message_id_not_belong_in_relevant_channel(register_user1, register_user2, user1_channel_message_id):

    user1_token = register_user1['token']
    message1_id = user1_channel_message_id

    user2_token = register_user2['token']
    assert user1_token != user2_token

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 400

# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 3.b) message_id exists but does not belong to DM that user is part of
    # User has global permission as "Member"
def test_message_edit_invalid_message_id_not_belong_in_relevant_DM_global_member(register_user1, register_user2, register_user3):

    user1_token = register_user1['token']

    user2_token = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    user3_token = register_user3['token']

    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [u_id2]
    })
    assert create_dm1.status_code == 200
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm1_id,
        'message': 'hello there from dm1'
    })
    assert send_dm1_message.status_code == 200
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user3_token,
        'message_id': message_id1,
        'message': 'hello there from dm1 [edited]'
    })
    assert edit_message.status_code == 400

# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 3.c) message_id exists but does not belong to DM that user is part of
    # User has global permission as "Owner"
    # Streams owners do not have owner permissions in DMs. 
    # The only users with owner permissions in DMs are the original creators of each DM.
def test_message_edit_invalid_message_id_not_belong_in_relevant_DM_global_owner(register_user1, register_user2, register_user3):

    user1_token = register_user1['token']

    user2_token = register_user2['token']

    u_id3 = register_user3['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user2_token,
        'u_ids': [u_id3]
    })
    assert create_dm1.status_code == 200
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm1_id,
        'message': 'hello there from dm1'
    })
    assert send_dm1_message.status_code == 200
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message_id1,
        'message': 'hello there from dm1 [edited]'
    })
    assert edit_message.status_code == 400

# Access error when:
    # the message was sent by an unauthorised user making this request
    # AND
    # the authorised user does NOT have owner permissions in the channel/DM
        # 1. User is member of channel but is not owner and did not send the message
        # that is being requested to edit
def test_message_edit_unauthorised_user_channel_not_send_message_and_not_owner(register_user1, register_user2, user1_channel_id, user1_channel_message_id):

    user1_token = register_user1['token']
    channel1_id = user1_channel_id

    user2_token = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'u_id': u_id2
    })

    message1_id = user1_channel_message_id

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 403

# Access error when:
    # the message was sent by an unauthorised user making this request
    # AND
    # the authorised user does NOT have owner permissions in the channel/DM
        # 2. User is member of DM but is not owner and did not send the message
        # that is being requested to edit

def test_message_edit_unauthorised_user_DM_not_send_message_and_not_owner(register_user1, register_user2, register_user3):

    user1_token = register_user1['token']

    user2_token = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    user3_token = register_user3['token']
    u_id3 = register_user3['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [u_id2, u_id3]
    })
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm1_id,
        'message': 'hello there from dm1'
    })
    assert send_dm1_message.status_code == 200
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user3_token,
        'message_id': message_id1,
        'message': 'hello there from dm1 [edited]'
    })
    assert edit_message.status_code == 403


##### Implementation #####

# Base valid case
def test_message_edit_basic_valid(register_user1, user1_channel_id, user1_channel_message_id):

    user1_token = register_user1['token']
    channel1_id = user1_channel_id
    message1_id =  user1_channel_message_id

    request_messages1 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert (json.loads(request_messages1.text)['messages'][0]['message'] == 'hello')

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 200

    request_messages2 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert (json.loads(request_messages2.text)['messages'][0]['message'] == 'hello [edited]')


# Message in channel was sent by the authorised user making this request
def test_message_edit_channel_authorised_user_request(register_user1, register_user2, user1_channel_id):

    user1_token = register_user1['token']
    channel1_id = user1_channel_id

    user2_token = register_user2['token']
    u_id2 = register_user2['auth_user_id']
    
    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'u_id': u_id2
    })

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'message': 'hello'
    })
    message2_id = json.loads(send_message2.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user2_token,
        'message_id': message2_id,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 200

# Message in DM sent by authorised user is being edited that user
def test_message_edit_DM_authorised_user_request(register_user1, register_user2, register_user3):

    user1_token = register_user1['token']

    user2_token =register_user2['token']
    u_id2 = register_user2['auth_user_id']

    u_id3 = register_user3['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [u_id2, u_id3]
    })
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm1_id,
        'message': 'hello there'
    })
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user2_token,
        'message_id': message_id1,
        'message': 'hello there [edited]'
    })
    assert edit_message.status_code == 200

# Message in channel is being edited by authorised user who has owner permissions
def test_message_edit_channel_owner_request(register_user1, register_user2):

    user1_token = register_user1['token']
    u_id1 = register_user1['auth_user_id']

    user2_token = register_user2['token']

    channel1 = requests.post(config.url + "channels/create/v2", json = {
        'token': user2_token,
        'name': 'anna_channel',
        'is_public': False
    })
    channel1_id = json.loads(channel1.text)['channel_id']

    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'u_id': u_id1
    })

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'hello'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    # Since user2 is the owner of 'anna_channel', user2 is able to edit user1's message in channel
    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'message': 'hello [edited]'
    })
    assert edit_message.status_code == 200

# Message in DM is being edited by authorised user who has owner permissions
def test_message_edit_DM_owner_request(register_user1, register_user2, register_user3):

    user1_token = register_user1['token']

    user2_token = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    u_id3 = register_user3['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [u_id2, u_id3]
    })
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': user2_token,
        'dm_id': dm1_id,
        'message': 'hello there'
    })
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message_id1,
        'message': 'hello there [edited]'
    })
    assert edit_message.status_code == 200

# Owner of UNSW Streams is able to edit message from any channel 
def test_message_edit_DM_global_owner_any_channel(register_user1, register_user2, register_user3):

    user1_token = register_user1['token']

    user2_token = register_user2['token']

    user3_token = register_user3['token']

    channel1 = requests.post(config.url + "channels/create/v2", json = {
        'token': user2_token,
        'name': 'sally_channel',
        'is_public': False
    })
    channel1_id = json.loads(channel1.text)['channel_id']

    channel2 = requests.post(config.url + "channels/create/v2", json = {
        'token': user3_token,
        'name': 'larry_channel',
        'is_public': True
    })
    channel2_id = json.loads(channel2.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'message': 'hello from user2'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user3_token,
        'channel_id': channel2_id,
        'message': 'hello from user3'
    })
    message2_id = json.loads(send_message2.text)['message_id']

    request_messages1 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user2_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert (json.loads(request_messages1.text)['messages'][0]['message'] == 'hello from user2')

    request_messages2 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user3_token,
        'channel_id': channel2_id,
        'start': 0
    })
    assert (json.loads(request_messages2.text)['messages'][0]['message'] == 'hello from user3')

    edit_message1 = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': 'hello there from user 2 [edited]'
    })
    assert edit_message1.status_code == 200

    edit_message2 = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message2_id,
        'message': 'hello there from user 3 [edited]'
    })
    assert edit_message2.status_code == 200

    # Checks that messages from user2 were edited by global owner of streams
    request_messages3 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user2_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert (json.loads(request_messages3.text)['messages'][0]['message'] == 'hello there from user 2 [edited]')

    # Checks that messages from user3 were edited by global owner of streams
    request_messages4 = requests.get(config.url + "channel/messages/v2", params = {
        'token': user3_token,
        'channel_id': channel2_id,
        'start': 0
    })
    assert (json.loads(request_messages4.text)['messages'][0]['message'] == 'hello there from user 3 [edited]')

# New message is empty, so the message is deleted in channel
def test_message_edit_channel_empty(register_user1, user1_channel_id, user1_channel_message_id):

    user1_token = register_user1['token']
    channel1_id = user1_channel_id

    user1_token = register_user1['token']
    channel1_id = user1_channel_id
    message1_id = user1_channel_message_id

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert len(json.loads(messages.text)['messages']) == 1

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': ''
    })
    assert edit_message.status_code == 200

    messages = requests.get(config.url + "channel/messages/v2", params = {
        'token': user1_token,
        'channel_id': channel1_id,
        'start': 0
    })
    assert len(json.loads(messages.text)['messages']) == 0
    
# New message is empty, so the message is deleted in dm
def test_message_edit_dm_empty(register_user1, register_user2):

    # Register users

    user1_token = register_user1['token']

    user2_id = register_user2['auth_user_id']

    # Create dm with user1 and user2
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id]
    })
    dm1_id = json.loads(dm1.text)['dm_id']

    # Send one message
    send_message1 = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm1_id,
        'message': 'hello'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    messages = requests.get(config.url + "dm/messages/v1", params = {
        'token': user1_token,
        'dm_id': dm1_id,
        'start': 0
    })
    assert len(json.loads(messages.text)['messages']) == 1

    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': ''
    })

    messages = requests.get(config.url + "dm/messages/v1", params = {
        'token': user1_token,
        'dm_id': dm1_id,
        'start': 0
    })
    assert len(json.loads(messages.text)['messages']) == 0
    assert edit_message.status_code == 200

## Removing message in a dm with 2 or more messages
def test_message_remove_dm_id_two_messages(register_user1, register_user2):
    # Registered users
    user1_token = register_user1['token']

    user2_id = register_user2['auth_user_id']
    
    # Created a dm
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id],
    })
    dm_id1 = json.loads(dm1.text)['dm_id']
    assert dm1.status_code == 200

    # User 1 sends 2 messages in the dm
    send_message1 = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm_id1,
        'message': 'hello1'
    })
    message1_id = json.loads(send_message1.text)['message_id']
    assert send_message1.status_code == 200

    send_message2 = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm_id1,
        'message': 'hello2'
    })
    assert send_message2.status_code == 200

    # User 1 tries to edit a message wihin channel
    edit_message = requests.put(config.url + "message/edit/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
        'message': ''
    })
    assert edit_message.status_code == 200
