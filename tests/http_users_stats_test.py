import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR

##########################################
############ users_stats tests ############
##########################################

# Access error: invalid token
def test_users_stats_invalid_token(global_owner):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == ACCESSERROR

# Test when the stream has no message, no dm, no channel
def test_users_stats_valid_user_no_channel_no_dm(global_owner):
    token = global_owner['token']

    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert len(json.loads(stats.text)['workspace_stats'][0]['channels_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][0]['num_channels_exist'] == 0
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][0]['time_stamp'] != 0

    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['workspace_stats'][0]['dms_exist']) == 1

    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['workspace_stats'][0]['messages_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['utilization_rate'] == 0.0

# Test when a channel is created in the stream
def test_users_stats_valid_user_one_channel(global_owner, create_channel):
    token = global_owner['token']
    assert create_channel['channel_id'] != None
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert len(json.loads(stats.text)['workspace_stats'][0]['channels_exist']) == 2
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][1]['num_channels_exist'] == 1
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][1]['time_stamp'] != 0

    assert len(json.loads(stats.text)['workspace_stats'][0]['dms_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][0]['time_stamp'] != 0

    assert len(json.loads(stats.text)['workspace_stats'][0]['messages_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['time_stamp'] != 0
    assert json.loads(stats.text)['workspace_stats'][0]['utilization_rate'] == 1.0

# Test when a DM is created in the stream
def test_users_stats_valid_user_one_dm(global_owner, create_dm):
    user1_token = global_owner['token']
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': user1_token
    })
    assert stats.status_code == VALID

    assert len(json.loads(stats.text)['workspace_stats'][0]['channels_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][0]['num_channels_exist'] == 0
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][0]['time_stamp'] != 0

    assert len(json.loads(stats.text)['workspace_stats'][0]['dms_exist']) == 2
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][1]['num_dms_exist'] == 1
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][1]['time_stamp'] != 0

    assert len(json.loads(stats.text)['workspace_stats'][0]['messages_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['time_stamp'] != 0

    assert json.loads(stats.text)['workspace_stats'][0]['utilization_rate'] == 1.0

# Test when a channel is created in the stream then user leaves channel. 
# workspace_stats channels should remain the same and utilisation rate is 0.0

# Test when a channel is created in the stream
def test_users_stats_valid_user_leave_channel(global_owner, create_channel):
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': channel_id
    })
    assert leave.status_code == VALID
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert len(json.loads(stats.text)['workspace_stats'][0]['channels_exist']) == 2
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][1]['num_channels_exist'] == 1
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['workspace_stats'][0]['channels_exist'][1]['time_stamp'] != 0

    assert len(json.loads(stats.text)['workspace_stats'][0]['dms_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['dms_exist'][0]['time_stamp'] != 0

    assert len(json.loads(stats.text)['workspace_stats'][0]['messages_exist']) == 1
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['workspace_stats'][0]['messages_exist'][0]['time_stamp'] != 0

    # the only user not in any channel or dm
    assert json.loads(stats.text)['workspace_stats'][0]['utilization_rate'] == 0.0

# When DM is created in the stream, then user removes DM
# user_stats DMs should decrease and utilisationn rate is 0.0
def test_users_stats_valid_user_remove_dm(global_owner, register_user2, create_dm):
    user1_token = global_owner['token']
    user2_token = register_user2['token']
    dm1_id = create_dm['dm_id']

    stats1 = requests.get(config.url + "users/stats/v1", params ={
        'token': user2_token
    })
    assert stats1.status_code == VALID
    assert len(json.loads(stats1.text)['workspace_stats'][0]['dms_exist']) == 2
    assert json.loads(stats1.text)['workspace_stats'][0]['utilization_rate'] == 1.0

    remove_dm = requests.delete(config.url + "dm/remove/v1", json = {
        'token': user1_token,
        'dm_id': dm1_id
    })

    stats2 = requests.get(config.url + "users/stats/v1", params ={
        'token': user2_token
    })
    assert stats2.status_code == VALID

    assert len(json.loads(stats2.text)['workspace_stats'][0]['channels_exist']) == 1
    assert json.loads(stats2.text)['workspace_stats'][0]['channels_exist'][0]['num_channels_exist'] == 0
    # test the timestamp is not equal to 0
    assert json.loads(stats2.text)['workspace_stats'][0]['channels_exist'][0]['time_stamp'] != 0

    assert len(json.loads(stats2.text)['workspace_stats'][0]['dms_exist']) == 3
    assert json.loads(stats2.text)['workspace_stats'][0]['dms_exist'][2]['num_dms_exist'] == 0
    assert json.loads(stats2.text)['workspace_stats'][0]['dms_exist'][2]['time_stamp'] != 0

    assert len(json.loads(stats2.text)['workspace_stats'][0]['messages_exist']) == 1
    assert json.loads(stats2.text)['workspace_stats'][0]['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats2.text)['workspace_stats'][0]['messages_exist'][0]['time_stamp'] != 0

    assert json.loads(stats2.text)['workspace_stats'][0]['utilization_rate'] == 0.0

# Message is sent in channel then message is removed
def test_users_stats_valid_user_send_and_remove_message(global_owner, create_channel):
    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    stats1 = requests.get(config.url + "users/stats/v1", params ={
        'token': user1_token
    })
    assert stats1.status_code == VALID

    assert json.loads(stats1.text)['workspace_stats'][0]['channels_exist'][1]['num_channels_exist'] == 1
    assert len(json.loads(stats1.text)['workspace_stats'][0]['channels_exist']) == 2
    # test the timestamp is not equal to 0
    assert json.loads(stats1.text)['workspace_stats'][0]['channels_exist'][1]['time_stamp'] != 0

    assert json.loads(stats1.text)['workspace_stats'][0]['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats1.text)['workspace_stats'][0]['dms_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats1.text)['workspace_stats'][0]['dms_exist']) == 1

    assert json.loads(stats1.text)['workspace_stats'][0]['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats1.text)['workspace_stats'][0]['messages_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats1.text)['workspace_stats'][0]['messages_exist']) == 1

    assert json.loads(stats1.text)['workspace_stats'][0]['utilization_rate'] == 1.0

    send_message = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'hello there'
    })
    message1_id = json.loads(send_message.text)['message_id']

    stats2 = requests.get(config.url + "users/stats/v1", params ={
        'token': user1_token
    })
    assert stats2.status_code == VALID
    assert len(json.loads(stats2.text)['workspace_stats'][0]['messages_exist']) == 2
    assert json.loads(stats2.text)['workspace_stats'][0]['messages_exist'][1]['num_messages_exist'] == 1
    assert json.loads(stats2.text)['workspace_stats'][0]['messages_exist'][1]['time_stamp'] != 1

    remove_message1 = requests.delete(config.url + "message/remove/v1", json = {
        'token': user1_token,
        'message_id': message1_id,
    })
    assert remove_message1.status_code == VALID

    stats3 = requests.get(config.url + "users/stats/v1", params ={
        'token': user1_token
    })
    assert stats3.status_code == VALID

    assert len(json.loads(stats3.text)['workspace_stats'][0]['channels_exist']) == 2
    assert json.loads(stats3.text)['workspace_stats'][0]['channels_exist'][1]['num_channels_exist'] == 1
    # test the timestamp is not equal to 0
    assert json.loads(stats3.text)['workspace_stats'][0]['channels_exist'][0]['time_stamp'] != 0

    assert len(json.loads(stats3.text)['workspace_stats'][0]['dms_exist']) == 1
    assert json.loads(stats3.text)['workspace_stats'][0]['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats3.text)['workspace_stats'][0]['dms_exist'][0]['time_stamp'] != 0

    assert json.loads(stats3.text)['workspace_stats'][0]['messages_exist'][2]['num_messages_exist'] == 0
    assert json.loads(stats3.text)['workspace_stats'][0]['messages_exist'][2]['time_stamp'] != 1
    assert len(json.loads(stats3.text)['workspace_stats'][0]['messages_exist']) == 3

    assert json.loads(stats3.text)['workspace_stats'][0]['utilization_rate'] == 1.0
