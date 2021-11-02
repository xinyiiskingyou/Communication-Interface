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

def test_valid_user_no_channel_no_dm(global_owner):
    token = global_owner['token']

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID

    assert (json.loads(stats.text) == {
        'channels_joined': [{
            'num_channels_joined':0,
            'time_stamp': 0
        }],
        'dms_joined:': [{
            'num_dms_joined': 0,
            'time_stamp': 0
        }],
        'messages_sent':[{
            'num_messages_sent': 0,
            'time_stamp':0
        }],
        'involvement_rate': 0
    })

def test_valid_user1(global_owner, create_channel, create_dm, user1_send_dm):
    token = global_owner['token']

    assert create_channel['channel_id'] != None
    assert create_dm['dm_id'] != None
    assert user1_send_dm != None

    stats = requests.get(config.url + "user/stats/v1", params ={
        'token': token
    })
    assert stats.status_code == VALID
    