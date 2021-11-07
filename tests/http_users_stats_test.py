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
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == ACCESSERROR

# Test when the stream has no message, no dm, no channel
def test_valid_user_no_channel_no_dm(global_owner):
    token = global_owner['token']

    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert json.loads(stats.text)['user_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert len(json.loads(stats.text)['user_stats']['channels_exist']) == 1
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['user_stats']['channels_exist'][0]['time_stamp'] != 0

    assert json.loads(stats.text)['user_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats.text)['user_stats']['dms_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['user_stats']['dms_exist']) == 1

    assert json.loads(stats.text)['user_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['user_stats']['messages_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['user_stats']['messages_exist']) == 1
    assert json.loads(stats.text)['user_stats']['utilization_rate'] == 0.0

# Test when a channel is created in the stream
def test_valid_user_one_channel(global_owner):
    token = global_owner['token']
    create_channel
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert json.loads(stats.text)['user_stats']['channels_exist'][1]['num_channels_exist'] == 1
    assert len(json.loads(stats.text)['user_stats']['channels_exist']) == 2
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['user_stats']['channels_exist'][1]['time_stamp'] != 0

    assert json.loads(stats.text)['user_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats.text)['user_stats']['dms_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['user_stats']['dms_exist']) == 1

    assert json.loads(stats.text)['user_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['user_stats']['messages_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['user_stats']['messages_exist']) == 1
    assert json.loads(stats.text)['user_stats']['utilization_rate'] == 1.0

# Test when a channel is created in the stream
def test_valid_user_leave_channel(global_owner):
    token = global_owner['token']
    channel_id = create_channel['channel_id']

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': channel_id
    })
    stats = requests.get(config.url + "users/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert json.loads(stats.text)['user_stats']['channels_exist'][1]['num_channels_exist'] == 1
    assert len(json.loads(stats.text)['user_stats']['channels_exist']) == 2
    # test the timestamp is not equal to 0
    assert json.loads(stats.text)['user_stats']['channels_exist'][1]['time_stamp'] != 0

    assert json.loads(stats.text)['user_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert json.loads(stats.text)['user_stats']['dms_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['user_stats']['dms_exist']) == 1

    assert json.loads(stats.text)['user_stats']['messages_exist'][0]['num_messages_exist'] == 0
    assert json.loads(stats.text)['user_stats']['messages_exist'][0]['time_stamp'] != 0
    assert len(json.loads(stats.text)['user_stats']['messages_exist']) == 1

    # the only user not in any channel or dm
    assert json.loads(stats.text)['user_stats']['utilization_rate'] == 0.0