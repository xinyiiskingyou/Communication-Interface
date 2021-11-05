import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel, user1_send_dm, create_dm
from tests.fixture import user1_handle_str, user2_handle_str, channel1_name, dm1_name, user3_handle_str
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

TAG_START = 0
TAG_END = 20

###############################################
########## notifications/get/v1 tests #########
###############################################

####### Tagged Notifications #######
def test_notifications_get_tagged_channel(global_owner, user1_handle_str, 
register_user2, user2_handle_str, create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    channel1_id = create_channel['channel_id']

    requests.post(config.url + "channel/join/v2", json = {
        'token': user2_token,
        'channel_id': channel1_id,
    })

    message = f'@{user2_handle_str} hello'

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
            'channel_id': channel1_id, 
            'dm_id': -1, 
            'notification_message': f"{user1_handle_str} tagged you in {channel1_name}: {message[TAG_START:TAG_END]}"
            },
        ]
    })

def test_notifications_get_tagged_DM(global_owner, user1_handle_str, register_user2, 
user2_handle_str, create_dm, dm1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    message = f'@{user2_handle_str} hello'

    send_message1 = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': create_dm['dm_id'],
        'message': message
    })
    assert send_message1.status_code == VALID


    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert len(json.loads(get_notifications.text)['notifications']) == 2

def test_notifications_get_tagged_multiple_same_user(global_owner, user1_handle_str, 
register_user2, user2_handle_str, create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    channel1_id = create_channel['channel_id']

    requests.post(config.url + "channel/join/v2", json = {
        'token': user2_token,
        'channel_id': channel1_id,
    })

    message = f'@{user2_handle_str} @{user2_handle_str} @{user2_handle_str} hello'

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })
    message1_id = json.loads(send_message1.text)['message_id']

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
                'channel_id': channel1_id, 
                'dm_id': -1, 
                'notification_message': f"{user1_handle_str} tagged you in {channel1_name}: {message[TAG_START:TAG_END]}"
            },
        ]
    })

def test_notifications_get_tagged_multiple_different_user(global_owner, user1_handle_str, 
register_user2, user2_handle_str, register_user3, user3_handle_str, create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    user3_token = register_user3['token']

    channel1_id = create_channel['channel_id']

    requests.post(config.url + "channel/join/v2", json = {
        'token': user2_token,
        'channel_id': channel1_id,
    })

    requests.post(config.url + "channel/join/v2", json = {
        'token': user3_token,
        'channel_id': channel1_id,
    })

    message = f'@{user2_handle_str} @{user3_handle_str} hello'

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })
    message1_id = json.loads(send_message1.text)['message_id']

    get_notifications1 = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications1.text) ==
    {
        'notifications': [
            {
                'channel_id': channel1_id, 
                'dm_id': -1, 
                'notification_message': f"{user1_handle_str} tagged you in {channel1_name}: {message[TAG_START:TAG_END]}"
            },
        ]
    })

    get_notifications2 = requests.get(config.url + "notifications/get/v1", params = {
        'token': user3_token
    })
    assert (json.loads(get_notifications2.text) ==
    {
        'notifications': [
            {
                'channel_id': channel1_id, 
                'dm_id': -1, 
                'notification_message': f"{user1_handle_str} tagged you in {channel1_name}: {message[TAG_START:TAG_END]}"
            },
        ]
    })

def test_notifications_get_tagged_not_member(global_owner, register_user2, 
user2_handle_str, create_channel):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    channel1_id = create_channel['channel_id']

    message = f'@{user2_handle_str} hello'

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })
    message1_id = json.loads(send_message1.text)['message_id']

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications.text) ==
        {
            'notifications': [],
        }
    )

def test_notifications_get_tagged_non_alphanumeric(global_owner, user1_handle_str, 
register_user2, user2_handle_str, create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    channel1_id = create_channel['channel_id']

    requests.post(config.url + "channel/join/v2", json = {
        'token': user2_token,
        'channel_id': channel1_id,
    })

    message = f'@{user2_handle_str}!@#$'

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
            'channel_id': channel1_id, 
            'dm_id': -1, 
            'notification_message': f"{user1_handle_str} tagged you in {channel1_name}: {message[TAG_START:TAG_END]}"
            },
        ]
    })

def test_notifications_get_tagged_gt_20_chars(global_owner, user1_handle_str, 
register_user2, user2_handle_str, create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    channel1_id = create_channel['channel_id']

    requests.post(config.url + "channel/join/v2", json = {
        'token': user2_token,
        'channel_id': channel1_id,
    })

    message = f'@{user2_handle_str}' + (' hello' * 10)

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
            'channel_id': channel1_id, 
            'dm_id': -1, 
            'notification_message': f"{user1_handle_str} tagged you in {channel1_name}: {message[TAG_START:TAG_END]}"
            },
        ]
    })

####### Reacted Notifications #######
def test_notifications_get_react_channel(global_owner, register_user2, user2_handle_str, 
create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    channel1_id = create_channel['channel_id']

    # User 2 joins channel1
    requests.post(config.url + "channel/join/v2", json = {
        'token': user2_token,
        'channel_id': channel1_id,
    })

    # User 1 sends message
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': 'react to message'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    # User 2 reacts to message
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user1_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
                'channel_id': channel1_id, 
                'dm_id': -1, 
                'notification_message': f"{user2_handle_str} reacted to your message in {channel1_name}"
            },
        ]
    })

def test_notifications_get_react_DM(global_owner, register_user2, user2_handle_str, 
create_dm, dm1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    dm1_id = create_dm['dm_id']

    # User 1 sends message
    send_message1 = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm1_id,
        'message': 'react to message'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    # User 2 reacts to message
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user1_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
                'channel_id': -1, 
                'dm_id': dm1_id, 
                'notification_message': f"{user2_handle_str} reacted to your message in {dm1_name}"
            },
        ]
    })

def test_notifications_get_react_DM_multiple(global_owner, register_user2, register_user3, create_dm):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    user3_token = register_user3['token']

    dm1_id = create_dm['dm_id']

    # User 1 sends message
    send_message1 = requests.post(config.url + "message/senddm/v1", json = {
        'token': user1_token,
        'dm_id': dm1_id,
        'message': 'react to message'
    })
    message1_id = json.loads(send_message1.text)['message_id']

    # User 2 reacts to message
    react1 = requests.post(config.url + "message/react/v1", json = {
        'token': user2_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert react1.status_code == VALID

    # User 3 reacts to message
    react2 = requests.post(config.url + "message/react/v1", json = {
        'token': user3_token,
        'message_id': message1_id,
        'react_id': 1
    })
    assert react2.status_code == VALID

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user1_token
    })
    assert len(json.loads(get_notifications.text)['notifications']) == 2


####### Added to Channel/DM Notifications #######
def test_notifications_get_add_channel(global_owner, register_user2, user1_handle_str, 
create_channel, channel1_name):

    user1_token = global_owner['token']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    channel1_id = create_channel['channel_id']

    # User 1 invites user 2 to channel1
    requests.post(config.url + "channel/invite/v2", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'u_id': user2_id
    })

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications.text) ==
    {
        'notifications': [
            {
                'channel_id': channel1_id, 
                'dm_id': -1, 
                'notification_message': f"{user1_handle_str} added you to {channel1_name}"
            },
        ]
    })

def test_notifications_get_add_DM(global_owner, register_user2, register_user3, user1_handle_str, 
create_dm, dm1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    user3_token = register_user3['token']

    dm1_id = create_dm['dm_id']

    get_notifications1 = requests.get(config.url + "notifications/get/v1", params = {
        'token': user1_token
    })
    assert (json.loads(get_notifications1.text) ==
    {
        'notifications': []
    })

    get_notifications2 = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert (json.loads(get_notifications2.text) ==
    {
        'notifications': [
            {
                'channel_id': -1, 
                'dm_id': dm1_id, 
                'notification_message': f"{user1_handle_str} added you to {dm1_name}"
            },
        ]
    })

    get_notifications3 = requests.get(config.url + "notifications/get/v1", params = {
        'token': user3_token
    })
    assert (json.loads(get_notifications3.text) ==
    {
        'notifications': [
            {
                'channel_id': -1, 
                'dm_id': dm1_id, 
                'notification_message': f"{user1_handle_str} added you to {dm1_name}"
            },
        ]
    })

# Mixed
def test_notifications_get_mixed(global_owner, user1_handle_str, register_user2, 
user2_handle_str, create_channel, channel1_name):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    channel1_id = create_channel['channel_id']

    # User 2 gets invited by user 1 to channel1
    requests.post(config.url + "channel/invite/v2", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'u_id': user2_id
    })

    message = f'@{user2_handle_str} hello'

    # User 1 tags user 2 in a message
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id,
        'message': message
    })
    message1_id = json.loads(send_message1.text)['message_id']

    # User 2 sends a message
    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel1_id,
        'message': 'react to this message'
    })
    message2_id = json.loads(send_message2.text)['message_id']

    # User 1 reacts to user 2's message
    react = requests.post(config.url + "message/react/v1", json = {
        'token': user1_token,
        'message_id': message2_id,
        'react_id': 1
    })
    assert react.status_code == VALID

    get_notifications = requests.get(config.url + "notifications/get/v1", params = {
        'token': user2_token
    })
    assert len(json.loads(get_notifications.text)['notifications']) == 3
    