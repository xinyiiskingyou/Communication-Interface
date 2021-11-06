import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
###### user_profile_set_name tests #######
##########################################

# Access error: invalid token
def test_user_name_invalid_token(global_owner):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': 'lee'
    })
    assert name.status_code == ACCESSERROR

# Input error when length of first name is < 1 or > 50
def test_user_name_invalid_name_first(global_owner):

    token = global_owner['token']

    # Invalid first name
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': '',
        'name_last': 'lee'
    })

    name1 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'a' * 51,
        'name_last': 'lee'
    })

    assert name.status_code == INPUTERROR
    assert name1.status_code == INPUTERROR

    # Access error: invalid token and invalid first name
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    name2 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': '',
        'name_last': 'lee'
    })

    name3 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'a' * 51,
        'name_last': 'lee'
    })
    assert name2.status_code == ACCESSERROR
    assert name3.status_code == ACCESSERROR
    
# Input error when length of first name is < 1 or > 50
def test_user_set_name_invalid_name_last(global_owner):

    token = global_owner['token']

    # Invalid last name
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': ''
    })

    name1 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': 'a' * 51
    })

    assert name.status_code == INPUTERROR
    assert name1.status_code == INPUTERROR

    # Access error: invalid token and invalid last name
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    name2 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': ''
    })

    name3 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': 'a' * 51
    })
    assert name2.status_code == ACCESSERROR
    assert name3.status_code == ACCESSERROR

##### Implementation #####

# Valid first name change 
def test_user_set_name_valid_name_first(global_owner, create_dm, create_channel):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    # Valid first name
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'lee'
    })

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })

    channel_id = create_channel['channel_id']
    dm_id = create_dm['dm_id']
   
    assert (json.loads(profile.text)['user'] == 
    {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'annabelle',
        'name_last': 'lee',
        'handle_str': 'annalee',
        'profile_img_url': 'profile_imgs/default_pic'
    })
    assert name.status_code == VALID

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': token,
        'channel_id': channel_id
    })
    member_name = json.loads(channel_details.text)['all_members'][0]['name_first']
    assert member_name == 'annabelle'
    owner_name = json.loads(channel_details.text)['all_members'][0]['name_first']
    assert owner_name == member_name

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['name_first'] == 'annabelle'

# Valid last name change
def test_user_set_name_valid_name_last(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    # Valid last name
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': 'park'
    })

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })
   
    assert (json.loads(profile.text)['user'] == 
    {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'park',
        'handle_str': 'annalee',
        'profile_img_url': 'profile_imgs/default_pic'
    })
    assert name.status_code == VALID

# Test the user's name has been changed in the channel
def test_user_set_name_valid_channel(global_owner):
    token = global_owner['token']

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': token,
        'name': '1531_CAMEL',
        'is_public': False
    })
    assert channel.status_code == VALID
    channel_id = json.loads(channel.text)['channel_id']
    
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'li'
    })
    assert name.status_code == VALID

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': token,
        'channel_id': channel_id
    })
    assert channel_details.status_code == VALID
    
    member_name = json.loads(channel_details.text)['all_members'][0]['name_last']
    assert member_name == 'li'
    owner_name = json.loads(channel_details.text)['all_members'][0]['name_last']
    assert owner_name == member_name

    member_name = json.loads(channel_details.text)['all_members'][0]['name_first']
    assert member_name == 'annabelle'
    owner_name = json.loads(channel_details.text)['all_members'][0]['name_first']
    assert owner_name == member_name

# Test the user's name has been changed in the dm
def test_user_set_name_valid_dm(global_owner, create_dm):

    token = global_owner['token']
    dm_id = create_dm['dm_id']

    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    assert name.status_code == VALID

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['name_first'] == 'emily'
    assert json.loads(dm_details.text)['members'][0]['name_last'] == 'wong'

# Valid first and last name change
def test_user_set_name_valid_name_first_and_last(global_owner):

    token = global_owner['token']
    u_id = global_owner['auth_user_id']

    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'parker'
    })

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })
   
    assert (json.loads(profile.text)['user'] == 
    {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'annabelle',
        'name_last': 'parker',
        'handle_str': 'annalee',
        'profile_img_url': 'profile_imgs/default_pic'
    })
    assert name.status_code == VALID

# User is not part of any channel or DM
def test_user_set_name_not_in_channel_DM(global_owner, register_user2):
    user1_token = global_owner['token']
    user1_id = global_owner['auth_user_id']
    user2_token = register_user2['token']

    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': user1_token,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    assert name.status_code == VALID

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': user1_token,
        'u_id': user1_id
    })

    assert (json.loads(profile.text)['user'] == 
    {
        'u_id': user1_id,
        'email': 'cat@gmail.com',
        'name_first': 'emily',
        'name_last': 'wong',
        'handle_str': 'annalee',
        'profile_img_url': 'profile_imgs/default_pic'
    })

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': '1531_CAMEL',
        'is_public': False
    })
    assert channel2.status_code == VALID
    channel_id = json.loads(channel2.text)['channel_id']

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': user2_token,
        'channel_id': channel_id
    })
    assert channel_details.status_code == VALID

# Change more then 2 users names in a dm
def test_user_set_name_valid_dm_2_members(global_owner, register_user2, create_dm):

    token1 = global_owner['token']
    token2 = register_user2['token']

    # User 1 cerates a dm with user 2
    dm_id1 = create_dm['dm_id']

    # User 1 changes name
    name1 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token1,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token1,
        'dm_id':  dm_id1
    })
    assert json.loads(dm_details.text)['members'][0]['name_first'] == 'emily'
    assert json.loads(dm_details.text)['members'][0]['name_last'] == 'wong'
    assert name1.status_code == VALID

    # User 2 changes name
    name2 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token2,
        'name_first': 'good',
        'name_last': 'luck'
    })
    assert name2.status_code == VALID

# Make creator of dm leave and change creators name
def test_user_set_name_valid_onwer_left(global_owner, register_user2, create_dm):

    token1 = global_owner['token']
    token2 = register_user2['token']

    # User 1 cerates a dm with user 2
    dm_id1 = create_dm['dm_id']

    # creator of dm leaves
    leave = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token1,
        'dm_id': dm_id1
    })
    assert leave.status_code == VALID

    # the creator of the dm who left changes name
    name1 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token1,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id':  dm_id1
    })
    assert json.loads(dm_details.text)['members'][0]['name_first'] == 'sally'
    assert json.loads(dm_details.text)['members'][0]['name_last'] == 'li'
    assert name1.status_code == VALID

# Change more then 2 users names in a channel
def test_user_set_name_valid_channel_2_members(global_owner, register_user2, create_channel):

    token1 = global_owner['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 creates a channel with user 2
    channel_id1 = create_channel['channel_id']

    # user 1 invites user 2
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token1,
        'channel_id': channel_id1,
        'u_id': u_id2
    })
    assert invite.status_code == VALID

    # User 1 changes name
    name1 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token1,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    assert name1.status_code == VALID

    # User 2 changes name
    name2 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token2,
        'name_first': 'good',
        'name_last': 'luck'
    })
    assert name2.status_code == VALID
