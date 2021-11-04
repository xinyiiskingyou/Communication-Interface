import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3, create_channel
from tests.fixture import user1_channel_message_id, user1_send_dm, create_dm
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

##########################################
##### user_profile_set_email tests #######
##########################################

# Access error: invalid token
def test_user_set_email_invalid_token(global_owner):

    token = global_owner['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'aaaa123@gmail.com'
    })
    assert mail.status_code == ACCESSERROR

# Input Error when email entered is not a valid email
def test_user_set_email_invalid_email(global_owner):

    token = global_owner['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'abc'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': '123.com'
    })
    assert mail.status_code == INPUTERROR
    assert mail1.status_code == INPUTERROR

    # Access error: invalid token and invalid email
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    mail2 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'abc'
    })

    mail3 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': '123.com'
    })
    assert mail2.status_code == ACCESSERROR
    assert mail3.status_code == ACCESSERROR

# Input error: email address is already being used by another user
def test_user_set_email_duplicate_email(global_owner, register_user2):

    user1_token = global_owner['token']
    user2_token = register_user2['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': user1_token,
        'email': 'elephant@gmail.com'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': user2_token,
        'email': 'cat@gmail.com'
    })
    assert mail.status_code == INPUTERROR
    assert mail1.status_code == INPUTERROR  

# valid case
def test_user_set_email_valid(global_owner):

    token = global_owner['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })
    assert mail.status_code == VALID

# Test the user's email has been changed in a channel
def test_user_set_email_valid_channel_coverage(global_owner):
    token = global_owner['token']

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': token,
        'name': '1531_CAMEL',
        'is_public': False
    })
    channel_id = json.loads(channel.text)['channel_id']
    assert channel_id > 0 

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })
    assert mail.status_code == VALID

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': token,
        'channel_id': channel_id
    })

    member_email = json.loads(channel_details.text)['all_members'][0]['email']
    assert member_email == 'comp1531@gmail.com'
    owner_email = json.loads(channel_details.text)['owner_members'][0]['email']
    assert owner_email == member_email

# Test the user's name has been changed in a dm
def test_user_set_email_valid_dm_coverage(global_owner, create_dm):
    token = global_owner['token']
    dm_id = create_dm['dm_id']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })
    assert mail.status_code == VALID

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['email'] == 'comp1531@gmail.com'

# Change more then 2 users email in a dm
def test_user_set_email_dm_2_members(global_owner, register_user2):

    token1 = global_owner['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 cerates a dm with user 2
    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token1,
        'u_ids': [u_id2]
    })
    assert dm1.status_code == VALID

    # User 1 changes email
    email1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'pain@gmail.com'
    })
    assert email1.status_code == VALID

    # User 2 changes email
    email2 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token2,
        'email': 'whyyyyy@gmail.com'
    })
    assert email2.status_code == VALID

# Make creator of dm leave and change creators email
def test_user_set_email_valid_onwer_left(global_owner, create_dm):

    token1 = global_owner['token']

    # User 1 cerates a dm with user 2
    dm_id1 = create_dm['dm_id']

    # creator of dm leaves
    leave = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token1,
        'dm_id': dm_id1
    })
    assert leave.status_code == VALID

    # the creator of the dm who left changes email
    email1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'pain@gmail.com'
    })
    assert email1.status_code == VALID

# Change more then 2 users email in a channel
def test_user_set_email_valid_channel_2_members(global_owner, register_user2, create_channel):

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

    # user 1 chnages email
    email1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'pain@gmail.com'
    })
    assert email1.status_code == VALID
    
    # user 2 changes email
    email2 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token2,
        'email': 'whyyyyy@gmail.com'
    })
    assert email2.status_code == VALID
