import pytest
import requests
import json
from src import config

@pytest.fixture
def setup():
    requests.delete(config.url + "clear/v1")

##########################################
########## message/edit/v1 tests #########
##########################################

# Input error when length of message is over 1000 characters
def test_message_edit_invalid_message_length(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message1_id,
            'message': 'a' * 1001
        }
    )
    assert edit_message.status_code == 400



# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 1. Negative message_id
def test_message_edit_invalid_message_id_negative(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    json.loads(send_message1.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': -1,
            'message': 'hello [edited]'
        }
    )
    assert edit_message.status_code == 400


# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 2. message_id is correct type (i.e. positive integer) but does not
    # exist with any message
def test_message_edit_invalid_message_id_nonexistant(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    json.loads(send_message1.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': 256,
            'message': 'hello [edited]'
        }
    )
    assert edit_message.status_code == 400


# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 3.a) message_id exists but does not belong to channel that user is part of
    # User has global permission of "Member"
def test_message_edit_invalid_message_id_not_belong_in_relevant_channel(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel1',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    channel2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user2_token,
            'name': 'sally_channel',
            'is_public': True
        }
    )
    channel2_id = json.loads(channel2.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    send_message2 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user2_token,
            'channel_id': channel2_id,
            'message': 'goodbye'
        }
    )
    json.loads(send_message2.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user2_token,
            'message_id': message1_id,
            'message': 'hello [edited]'
        }
    )
    assert edit_message.status_code == 400


# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 3.b) message_id exists but does not belong to DM that user is part of
    # User has global permission as "Member"
def test_message_edit_invalid_message_id_not_belong_in_relevant_DM_global_member(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'larry@gmail.com',
            'password': 'password',
            'name_first': 'larry',
            'name_last': 'li'
        }
    )
    user3_token = json.loads(user3.text)['token']

    create_dm1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': [u_id2]
        })
    assert create_dm1.status_code == 200
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there from dm1'
        }
    )
    assert send_dm1_message.status_code == 200
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user3_token,
            'message_id': message_id1,
            'message': 'hello there from dm1 [edited]'
        }
    )
    assert edit_message.status_code == 400


# Input error when message_id does not refer to a valid message 
# within a channel/DM that the authorised user has joined
    # 3.b) message_id exists but does not belong to DM that user is part of
    # User has global permission as "Owner"
    # Streams owners do not have owner permissions in DMs. 
    # The only users with owner permissions in DMs are the original creators of each DM.
def test_message_edit_invalid_message_id_not_belong_in_relevant_DM_global_owner(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'larry@gmail.com',
            'password': 'password',
            'name_first': 'larry',
            'name_last': 'li'
        }
    )
    user3_token = json.loads(user3.text)['token']
    user3_data = user3.json()
    u_id3 = user3_data['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user2_token,
            'u_ids': [u_id3]
        })
    assert create_dm1.status_code == 200
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there from dm1'
        }
    )
    assert send_dm1_message.status_code == 200
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message_id1,
            'message': 'hello there from dm1 [edited]'
        }
    )
    assert edit_message.status_code == 400


# Access error when:
    # the message was sent by an unauthorised user making this request
    # AND
    # the authorised user does NOT have owner permissions in the channel/DM
        # 1. User is member of channel but is not owner and did not send the message
        # that is being requested to edit
def test_message_edit_unauthorised_user_channel_not_send_message_and_not_owner(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel1',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    requests.post(config.url + 'channel/invite/v2', 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'u_id': u_id2
        }
    )

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user2_token,
            'message_id': message1_id,
            'message': 'hello [edited]'
        }
    )
    assert edit_message.status_code == 403


# Access error when:
    # the message was sent by an unauthorised user making this request
    # AND
    # the authorised user does NOT have owner permissions in the channel/DM
        # 2. User is member of DM but is not owner and did not send the message
        # that is being requested to edit

def test_message_edit_unauthorised_user_DM_not_send_message_and_not_owner(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'larry@gmail.com',
            'password': 'password',
            'name_first': 'larry',
            'name_last': 'li'
        }
    )
    user3_token = json.loads(user3.text)['token']
    user3_data = user3.json()
    u_id3 = user3_data['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': [u_id2, u_id3]
        })
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there from dm1'
        }
    )
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user3_token,
            'message_id': message_id1,
            'message': 'hello there from dm1 [edited]'
        }
    )
    assert edit_message.status_code == 403



##### Implementation #####

# Base valid case
def test_message_edit_basic_valid(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    request_messages1 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert (json.loads(request_messages1.text)['messages'][0]['message'] == 'hello')

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message1_id,
            'message': 'hello [edited]'
        }
    )
    assert edit_message.status_code == 200

    request_messages2 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert (json.loads(request_messages2.text)['messages'][0]['message'] == 'hello [edited]')
    
    

# Message in channel was sent by the authorised user making this request
def test_message_edit_channel_authorised_user_request(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    requests.post(config.url + 'channel/invite/v2', 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'u_id': u_id2
        }
    )

    send_message2 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user2_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message2_id = json.loads(send_message2.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user2_token,
            'message_id': message2_id,
            'message': 'hello [edited]'
        }
    )
    assert edit_message.status_code == 200


# Message in DM sent by authorised user is being edited that user
def test_message_edit_DM_authorised_user_request(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'larry@gmail.com',
            'password': 'password',
            'name_first': 'larry',
            'name_last': 'li'
        }
    )
    json.loads(user3.text)['token']
    user3_data = user3.json()
    u_id3 = user3_data['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': [u_id2, u_id3]
        })
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user2_token,
            'message_id': message_id1,
            'message': 'hello there [edited]'
        }
    )
    assert edit_message.status_code == 200


# Message in channel is being edited by authorised user who has owner permissions
def test_message_edit_channel_owner_request(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']
    user1_data = user1.json()
    u_id1 = user1_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user2_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    requests.post(config.url + 'channel/invite/v2', 
        json = {
            'token': user2_token,
            'channel_id': channel1_id,
            'u_id': u_id1
        }
    )

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    # Since user2 is the owner of 'anna_channel', user2 is able to edit user1's message in channel
    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user2_token,
            'message_id': message1_id,
            'message': 'hello [edited]'
        }
    )

    assert edit_message.status_code == 200


# Message in DM is being edited by authorised user who has owner permissions
def test_message_edit_DM_owner_request(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'larry@gmail.com',
            'password': 'password',
            'name_first': 'larry',
            'name_last': 'li'
        }
    )
    json.loads(user3.text)['token']
    user3_data = user3.json()
    u_id3 = user3_data['auth_user_id']

    create_dm1 = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': [u_id2, u_id3]
        })
    dm1_id = json.loads(create_dm1.text)['dm_id']

    send_dm1_message = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    message_id1 = json.loads(send_dm1_message.text)['message_id']

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message_id1,
            'message': 'hello there [edited]'
        }
    )
    assert edit_message.status_code == 200


# Owner of UNSW Streams is able to edit message from any channel 
def test_message_edit_DM_global_owner_any_channel(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'larry@gmail.com',
            'password': 'password',
            'name_first': 'larry',
            'name_last': 'li'
        }
    )
    user3_token = json.loads(user3.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user2_token,
            'name': 'sally_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    channel2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user3_token,
            'name': 'larry_channel',
            'is_public': True
        }
    )
    channel2_id = json.loads(channel2.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user2_token,
            'channel_id': channel1_id,
            'message': 'hello from user2'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    send_message2 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user3_token,
            'channel_id': channel2_id,
            'message': 'hello from user3'
        }
    )
    message2_id = json.loads(send_message2.text)['message_id']

    request_messages1 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user2_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert (json.loads(request_messages1.text)['messages'][0]['message'] == 'hello from user2')

    request_messages2 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user3_token,
            'channel_id': channel2_id,
            'start': 0
        }
    )
    assert (json.loads(request_messages2.text)['messages'][0]['message'] == 'hello from user3')

    edit_message1 = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message1_id,
            'message': 'hello there from user 2 [edited]'
        }
    )
    assert edit_message1.status_code == 200

    edit_message2 = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message2_id,
            'message': 'hello there from user 3 [edited]'
        }
    )
    assert edit_message2.status_code == 200

    # Checks that messages from user2 were edited by global owner of streams
    request_messages3 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user2_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert (json.loads(request_messages3.text)['messages'][0]['message'] == 'hello there from user 2 [edited]')

    # Checks that messages from user3 were edited by global owner of streams
    request_messages4 = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user3_token,
            'channel_id': channel2_id,
            'start': 0
        }
    )
    assert (json.loads(request_messages4.text)['messages'][0]['message'] == 'hello there from user 3 [edited]')



# New message is empty, so the message is deleted
def test_message_edit_empty(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': user1_token,
            'name': 'anna_channel',
            'is_public': False
        }
    )
    channel1_id = json.loads(channel1.text)['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", 
        json = {
            'token': user1_token,
            'channel_id': channel1_id,
            'message': 'hello'
        }
    )
    message1_id = json.loads(send_message1.text)['message_id']

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert len(json.loads(messages.text)['messages']) == 1

    edit_message = requests.put(config.url + "message/edit/v1", 
        json = {
            'token': user1_token,
            'message_id': message1_id,
            'message': ''
        }
    )

    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': user1_token,
            'channel_id': channel1_id,
            'start': 0
        }
    )
    assert len(json.loads(messages.text)['messages']) == 0
    assert edit_message.status_code == 200

