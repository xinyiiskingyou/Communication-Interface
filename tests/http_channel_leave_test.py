import pytest 
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, create_channel
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
########## channel_leave tests ###########
##########################################

# Access error: invalid token
def test_leave_invalid_token(global_owner, create_channel):

    token = global_owner['token']
    channel_id = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': channel_id
    }) 
    assert leave.status_code == ACCESSERROR

# Invalid channel_id 
def test_invalid_leave_channel_id(global_owner):

    token = global_owner['token']

    # Input error: invalid channel_id
    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': -1
    }) 
    assert leave.status_code == INPUTERROR

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': ''
    }) 
    assert leave.status_code == INPUTERROR

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    leave1 = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': -1
    }) 
    assert leave1.status_code == ACCESSERROR

# Access error: valid channel_idd but the authorised user is not a member of the channel
def test_invalid_leave_not_member(register_user2, create_channel):

    # token doesn't not refer to any member in this channel
    token = register_user2['token']
    channel_id1 = create_channel['channel_id']

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': channel_id1
    }) 
    assert leave.status_code == ACCESSERROR

    user1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'anna@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user1_token = json.loads(user1.text)['token']
    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': user1_token, 
        'channel_id': channel_id1
    }) 
    assert leave.status_code == ACCESSERROR

###### Implementation ######

# Valid case: remove the member of the channel
def test_channel_leave_valid(global_owner, register_user2, create_channel): 

    token1 = global_owner['token']
    token2 = register_user2['token']
    assert token1 != token2
    channel_id1 = create_channel['channel_id']

    # token2 joins the channel
    join = requests.post(config.url + "channel/join/v2", json ={ 
        'token': token2, 
        'channel_id': channel_id1
    })   
    assert join.status_code == VALID

    # token2 as a member leaves the channel
    respo = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token2, 
        'channel_id': channel_id1
    })  
    assert respo.status_code == VALID

# Valid case: remove the only owner of the channel and the channel will remain
def test_channel_leave_valid1(global_owner, register_user2, create_channel): 

    token1 = global_owner['token']
    token2 = register_user2['token']

    channel_id1 = create_channel['channel_id']

    # token2 joins the channel
    respo1 = requests.post(config.url + "channel/join/v2", json ={ 
        'token': token2, 
        'channel_id': channel_id1
    })   
    assert respo1.status_code == VALID

    # the only owner leaves the channel
    respo = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token1, 
        'channel_id': channel_id1
    })  
    assert respo.status_code == VALID

# Valid case: The only channel owner leaves and rejoins the channel as a member
def test_owner_leave_add(global_owner, register_user2, create_channel): 
    token1 = global_owner['token']
    token2 = register_user2['token']

    channel_id1 = create_channel['channel_id']

    # token2 joins to the channel
    respo1 = requests.post(config.url + "channel/join/v2", json ={ 
        'token': token2, 
        'channel_id': channel_id1
    })   
    assert respo1.status_code == VALID

    # the only owner token1 leaves the channel
    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token1, 
        'channel_id': channel_id1
    })  
    assert leave.status_code == VALID

    # token1 rejoins the channel and is the member of channel
    # token1 is not a owner of the channel
    join = requests.post(config.url + "channel/join/v2", json = { 
        'token': token1, 
        'channel_id': channel_id1
    })
    assert join.status_code == VALID 

    details = requests.get(config.url + "channel/details/v2", params = { 
        'token': token1, 
        'channel_id': channel_id1
    })

    member_list = json.loads(details.text)['all_members']
    assert len(member_list) == 2
    owner_list = json.loads(details.text)['owner_members']
    assert len(owner_list) == 0
