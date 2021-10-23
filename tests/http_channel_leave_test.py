import pytest 
import requests
import json
from requests.api import request 
from src import config

@pytest.fixture
def register_user():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user1():
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    return user1_data

@pytest.fixture
def create_channel(register_user):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user['token'],
        'name': 'anna',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data

##########################################
########## channel_leave tests ###########
##########################################

# Access error: invalid token
def test_leave_invalid_token(register_user, create_channel):

    token = register_user['token']
    channel_id = create_channel['channel_id']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': channel_id
    }) 
    assert leave.status_code == 403

# Invalid channel_id 
def test_invalid_leave_channel_id(register_user):

    token = register_user['token']

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': -1
    }) 
    assert leave.status_code == 400

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': ''
    }) 
    assert leave.status_code == 400

    # access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    leave1 = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': -1
    }) 
    assert leave1.status_code == 403

# channel_id is valid and the authorised user is not a member of the channel
def test_invalid_leave_not_member(register_user1, create_channel):

    token = register_user1['token']
    channel_id1 = create_channel['channel_id']

    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token, 
        'channel_id': channel_id1
    }) 
    assert leave.status_code == 403

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
    assert leave.status_code == 403

###### Implementation ######
# remove the member of the channel
def test_channel_leave_valid(register_user, register_user1, create_channel): 

    token1 = register_user['token']
    token2 = register_user1['token']
    assert token1 != token2
    channel_id1 = create_channel['channel_id']

    # add token2 to the channel
    join = requests.post(config.url + "channel/join/v2", json ={ 
        'token': token2, 
        'channel_id': channel_id1
    })   
    assert join.status_code == 200

    # token2 as a member leaves the channel
    respo = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token2, 
        'channel_id': channel_id1
    })  
    assert respo.status_code == 200

# remove the only owner of the channel and the channel will remain
def test_channel_leave_valid1(register_user, register_user1, create_channel): 

    token1 = register_user['token']
    token2 = register_user1['token']

    channel_id1 = create_channel['channel_id']

    # add token2 to the channel
    respo1 = requests.post(config.url + "channel/join/v2", json ={ 
        'token': token2, 
        'channel_id': channel_id1
    })   
    assert respo1.status_code == 200

    # the only owner leaves the channel
    respo = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token1, 
        'channel_id': channel_id1
    })  
    assert respo.status_code == 200

def test_owner_leave_add(register_user, register_user1, create_channel): 
    token1 = register_user['token']
    token2 = register_user1['token']

    channel_id1 = create_channel['channel_id']

        # add token2 to the channel
    respo1 = requests.post(config.url + "channel/join/v2", json ={ 
        'token': token2, 
        'channel_id': channel_id1
    })   
    assert respo1.status_code == 200

    # the only owner leaves the channel
    leave = requests.post(config.url + "channel/leave/v1",json = { 
        'token': token1, 
        'channel_id': channel_id1
    })  
    assert leave.status_code == 200

    join = requests.post(config.url + "channel/join/v2", json = { 
        'token': token1, 
        'channel_id': channel_id1
    })
    assert join.status_code == 200 

    details = requests.get(config.url + "channel/details/v2", params = { 
        'token': token1, 
        'channel_id': channel_id1
    })

    member_list = json.loads(details.text)['all_members']
    assert len(member_list) == 2
    owner_list = json.loads(details.text)['owner_members']
    assert len(owner_list) == 0
