import pytest
import requests
import json
from src import config

VALID = 200
ACCESSERROR = 403
INPUTERROR = 400

DEFAULT_IMG_URL = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

@pytest.fixture
def global_owner():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cat@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    return user_data

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
    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'kellyh@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user3_data = user3.json()
    return user3_data

# global owner creates a channel
@pytest.fixture
def create_channel(global_owner):
    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': global_owner['token'],
        'name': 'anna',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data

# global owner sends a message in channel
@pytest.fixture
def user1_channel_message_id(global_owner, create_channel):

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': global_owner['token'],
        'channel_id': create_channel['channel_id'],
        'message': 'hello'
    })
    message1_id = json.loads(send_message1.text)['message_id']
    return message1_id

# global owner creates a dm
@pytest.fixture
def create_dm(global_owner, register_user2, register_user3):
    token = global_owner['token']
    u_id2 = register_user2['auth_user_id']
    u_id3 = register_user3['auth_user_id']
    dm = requests.post(config.url + "dm/create/v1", json = {
        'token': token,
        'u_ids': [u_id2, u_id3]
    })
    assert dm.status_code == VALID
    dm_data = dm.json()
    return dm_data

# global owner sends a message in dm
@pytest.fixture
def user1_send_dm(global_owner, create_dm):
    send_dm1_message = requests.post(config.url + "message/senddm/v1", json = {
        'token': global_owner['token'],
        'dm_id': create_dm['dm_id'],
        'message': 'hello'
    })
    assert send_dm1_message.status_code == VALID
    dm_message_id = json.loads(send_dm1_message.text)['message_id']
    return dm_message_id

###### notifications ######
# gets the handle_str of user 1 (global owner)
@pytest.fixture
def user1_handle_str(global_owner):
    use1_profile = requests.get(config.url + "user/profile/v1", params = {
        'token': global_owner['token'], 
        'u_id': global_owner['auth_user_id'], 
    })
    user1_handle_str = json.loads(use1_profile.text)['user']['handle_str']
    return user1_handle_str

# gets the handle_str of user 2
@pytest.fixture
def user2_handle_str(register_user2):
    use2_profile = requests.get(config.url + "user/profile/v1", params = {
        'token': register_user2['token'], 
        'u_id': register_user2['auth_user_id'], 
    })
    user2_handle_str = json.loads(use2_profile.text)['user']['handle_str']
    return user2_handle_str
    
# gets the handle_str of user 3
@pytest.fixture
def user3_handle_str(register_user3):
    use3_profile = requests.get(config.url + "user/profile/v1", params = {
        'token': register_user3['token'], 
        'u_id': register_user3['auth_user_id'], 
    })
    user3_handle_str = json.loads(use3_profile.text)['user']['handle_str']
    return user3_handle_str

# get channel name of global_owner's channel
@pytest.fixture
def channel1_name(global_owner, create_channel):
    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': global_owner['token'], 
        'channel_id': create_channel['channel_id'], 
    })
    channel_name = json.loads(channel_details.text)['name']
    return channel_name

# get dm name of global_onwer's DM
@pytest.fixture
def dm1_name(global_owner, create_dm):
    dm_details = requests.get(config.url + "dm/details/v1", params = {
        'token': global_owner['token'], 
        'dm_id': create_dm['dm_id'], 
    })
    assert dm_details.status_code == VALID
    dm_name = json.loads(dm_details.text)['name']
    return dm_name