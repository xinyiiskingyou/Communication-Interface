import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR

##########################################
############ user_stats tests ############
##########################################

# Access error: invalid token
def test_user_stats_invalid_token(global_owner):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == ACCESSERROR

# Test when the user did not join any channel or dm
def test_valid_user_no_channel_no_dm(global_owner):
    token = global_owner['token']

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert json.loads(stats.text)['user_stats']['channels_joined'][0]['num_channels_joined'] == 0
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['user_stats']['channels_joined'][0]['time_stamp'] != 0
    assert json.loads(stats.text)['user_stats']['dms_joined'][0]['num_dms_joined'] == 0
    assert json.loads(stats.text)['user_stats']['messages_sent'][0]['num_messages_sent'] == 0
    assert json.loads(stats.text)['user_stats']['involvement_rate'] == 0.0

# Tests when the user only join the channel
def test_valid_user_only_join_channel(global_owner, create_channel):
    token = global_owner['token']

    assert create_channel['channel_id'] != None

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    # user 1 joins a channel
    # since the list starts with 0, the length will always start with 1
    assert len(json.loads(stats.text)['user_stats']['channels_joined']) == 2
    assert len(json.loads(stats.text)['user_stats']['dms_joined']) == 1
    assert len(json.loads(stats.text)['user_stats']['messages_sent']) == 1
    assert json.loads(stats.text)['user_stats']['involvement_rate'] != 0

# Tests the length when the user leaves the channel
def test_valid_user_rejoin_channel(global_owner, create_channel):
    token = global_owner['token']

    # user leaves the channel
    respo = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': create_channel['channel_id']
    })  
    assert respo.status_code == VALID

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['channels_joined']) == 1

    # user rejoins the channel
    rejoin = requests.post(config.url + "channel/join/v2", json = { 
        'token': token, 
        'channel_id': create_channel['channel_id']
    })
    assert rejoin.status_code == VALID
    
    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['channels_joined']) == 2

# Tests when the user only join the dm
def test_valid_user_only_join_dm(global_owner, create_dm):

    token = global_owner['token']
    assert create_dm['dm_id'] != None

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    # user 1 joins a channel
    # since the list starts with 0, the length will always start with 1
    assert len(json.loads(stats.text)['user_stats']['channels_joined']) == 1
    assert len(json.loads(stats.text)['user_stats']['dms_joined']) == 2
    assert len(json.loads(stats.text)['user_stats']['messages_sent']) == 1
    assert json.loads(stats.text)['user_stats']['involvement_rate'] != 0

# Test the length when the user remove dm
def test_valid_user_remove_dm(global_owner, create_dm):

    token = global_owner['token']
    resp1 = requests.delete(config.url + "dm/remove/v1", json = {
        'token': token,
        'dm_id': create_dm['dm_id']
    })
    assert resp1.status_code == VALID

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['dms_joined']) == 1

# Test the length when the user leave dm
def test_valid_user_remove_dm(global_owner, create_dm):

    token = global_owner['token']
    resp1 = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token, 
        'dm_id': create_dm['dm_id']
    })  
    assert resp1.status_code == VALID

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['dms_joined']) == 1

# Tests when the user sends a message in dm and channel
def test_valid_user_send_message(global_owner, user1_send_dm, user1_channel_message_id):
    
    token = global_owner['token']
    # user 1 send a message in dm and channel
    assert user1_send_dm != None
    assert user1_channel_message_id != None

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    # user 1 joins a channel and a dm
    assert len(json.loads(stats.text)['user_stats']['channels_joined']) == 2
    assert len(json.loads(stats.text)['user_stats']['dms_joined']) == 2
    # messages_sent length will be 3
    assert len(json.loads(stats.text)['user_stats']['messages_sent']) == 3
    assert json.loads(stats.text)['user_stats']['involvement_rate'] != 0

# Test the number of the message the user sent will not decrease
def test_valid_message_length(global_owner, user1_channel_message_id, create_channel):

    token = global_owner['token']
    # user sent a message
    assert user1_channel_message_id != None
    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['messages_sent']) == 2

    # remove a message
    remove_message1 = requests.delete(config.url + "message/remove/v1", json = {
        'token': token,
        'message_id': user1_channel_message_id,
    })
    assert remove_message1.status_code == VALID

    # test the number will not decrease 
    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['messages_sent']) == 2

    # user1 sends a message again
    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': token,
        'channel_id': create_channel['channel_id'], 
        'message': 'hello there'
    })
    assert send_message.status_code == VALID

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert len(json.loads(stats.text)['user_stats']['messages_sent']) == 3

    # but the total number of message will decreased
    messages = requests.get(config.url + "channel/messages/v2", params ={
        'token': token,
        'channel_id': create_channel['channel_id'],
        'start': 0
    })
    assert len(json.loads(messages.text)['messages']) == 1

    assert json.loads(stats.text)['user_stats']['involvement_rate'] == 1.0

# Test the range of involvement rate is between 0 to 1
def test_valid_involvement_rate_less_than_1(global_owner, register_user2, create_channel):
    # user1 creates a channel
    token = global_owner['token']
    assert create_channel['channel_id'] != None

    # user2 creates 2 channels
    requests.post(config.url + "channels/create/v2", json ={
        'token': register_user2['token'],
        'name': 'anna',
        'is_public': True
    })

    requests.post(config.url + "channels/create/v2", json ={
        'token': register_user2['token'],
        'name': 'anna1',
        'is_public': True
    })

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    assert json.loads(stats.text)['user_stats']['involvement_rate'] < 1
    assert json.loads(stats.text)['user_stats']['involvement_rate'] > 0
