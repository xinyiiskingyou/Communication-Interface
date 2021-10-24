import pytest
import requests
import json
from src import config 

@pytest.fixture
def register_user1():
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
def user1_channel_id(register_user1):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user1['token'],
        'name': 'anna',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data['channel_id']

@pytest.fixture
def user1_dm_id(register_user1, register_user2):

    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': register_user1['token'],
        'u_ids': [register_user2['auth_user_id']]
    })
    dm_id = json.loads(dm1.text)['dm_id']
    return dm_id

##########################################
############ users_all tests #############
##########################################

# Access error when invalid token
def test_user_all_invalid_token(register_user1):
    token = register_user1['token']

    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    all1 = requests.get(config.url + "users/all/v1", params ={
        'token': token
    })
    assert all1.status_code == 403

# Valid case when there is only 1 user
def test_user_all_1_member(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']
    all1 = requests.get(config.url + "users/all/v1", params ={
        'token': token
    })
    assert all1.status_code == 200

    assert (json.loads(all1.text)['users'] == 
    [{
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'lee',
        'handle_str': 'annalee'
    }])
    assert len(json.loads(all1.text)) == 1

# Valid case when there is more then 1 user
def test_user_all_several_members(register_user1, register_user2):

    token1 = register_user1['token']
    token2 = register_user2['token']

    all1 = requests.get(config.url + "users/all/v1", params ={
        'token': token1
    })

    all2 = requests.get(config.url + "users/all/v1", params ={
        'token': token2
    })

    # test using length of list as cannot be certain 
    # the listed order of users
    assert len(json.loads(all1.text)['users']) == 2
    assert len(json.loads(all2.text)['users']) == 2
    assert len(json.loads(all1.text)['users']) == len(json.loads(all2.text)['users'])

##########################################
########## user_profile tests ############
##########################################

# Access error when invalid token
def test_user_profile_invalid_token(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    profile1 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })
    assert profile1.status_code == 403

# Input error for invalid u_id
def test_user_profile_invalid_u_id(register_user1):

    token = register_user1['token']

    profile1 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': -1
    })

    profile2 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': 0
    })

    profile3 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': 256
    })

    assert profile1.status_code == 400
    assert profile2.status_code == 400
    assert profile3.status_code == 400

    # Access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    profile4 = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': -1
    })
    assert profile4.status_code == 403

##### Implementation #####

# Valid Case for looking at own profile
def test_user_profile_valid_own(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })

    assert profile.status_code == 200
    assert (json.loads(profile.text)['user'] == 
        {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'lee',
        'handle_str': 'annalee'
    })

# Valid Case for looking at someone else's profile
def test_user_profile_valid_someone_else(register_user1, register_user2):

    token = register_user1['token']
    u_id2 = (register_user2['auth_user_id'])

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id2
    })

    assert profile.status_code == 200
    assert (json.loads(profile.text)['user'] == 
        {
        'u_id': u_id2,
        'email': 'elephant@gmail.com',
        'name_first': 'sally',
        'name_last': 'li',
        'handle_str': 'sallyli'
    })

##########################################
###### user_profile_set_name tests #######
##########################################

# Access error: invalid token
def test_user_name_invalid_token(register_user1):

    token = register_user1['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'anna',
        'name_last': 'lee'
    })
    assert name.status_code == 403

# Input error when length of first name is < 1 or > 50
def test_user_name_invalid_name_first(register_user1):

    token = register_user1['token']

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

    assert name.status_code == 400
    assert name1.status_code == 400

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
    assert name2.status_code == 403
    assert name3.status_code == 403
    
# Input error when length of first name is < 1 or > 50
def test_user_set_name_invalid_name_last(register_user1):

    token = register_user1['token']

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

    assert name.status_code == 400
    assert name1.status_code == 400

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
    assert name2.status_code == 403
    assert name3.status_code == 403

##### Implementation #####

# Valid first name change 
def test_user_set_name_valid_name_first(register_user1, user1_dm_id, user1_channel_id):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']

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

    channel_id = user1_channel_id
    dm_id = user1_dm_id
   
    assert (json.loads(profile.text)['user'] == 
    {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'annabelle',
        'name_last': 'lee',
        'handle_str': 'annalee'
    })
    assert name.status_code == 200

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
def test_user_set_name_valid_name_last(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']

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
        'handle_str': 'annalee'
    })
    assert name.status_code == 200

# Test the user's name has been changed in the channel
def test_user_set_name_valid_channel(register_user1):
    token = register_user1['token']

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': token,
        'name': '1531_CAMEL',
        'is_public': False
    })
    assert channel.status_code == 200
    channel_id = json.loads(channel.text)['channel_id']
    
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'li'
    })
    assert name.status_code == 200

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': token,
        'channel_id': channel_id
    })
    assert channel_details.status_code == 200
    
    member_name = json.loads(channel_details.text)['all_members'][0]['name_last']
    assert member_name == 'li'
    owner_name = json.loads(channel_details.text)['all_members'][0]['name_last']
    assert owner_name == member_name

    member_name = json.loads(channel_details.text)['all_members'][0]['name_first']
    assert member_name == 'annabelle'
    owner_name = json.loads(channel_details.text)['all_members'][0]['name_first']
    assert owner_name == member_name

# Test the user's name has been changed in the dm
def test_user_set_name_valid_dm(register_user1, user1_dm_id):

    token = register_user1['token']
    dm_id = user1_dm_id

    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    assert name.status_code == 200

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['name_first'] == 'emily'
    assert json.loads(dm_details.text)['members'][0]['name_last'] == 'wong'

# Valid first and last name change
def test_user_set_name_valid_name_first_and_last(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']

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
        'handle_str': 'annalee'
    })
    assert name.status_code == 200

# User is not part of any channel or DM
def test_user_set_name_not_in_channel_DM(register_user1, register_user2):
    user1_token = register_user1['token']
    user1_id = register_user1['auth_user_id']
    user2_token = register_user2['token']

    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': user1_token,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    assert name.status_code == 200

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
        'handle_str': 'annalee'
    })

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': '1531_CAMEL',
        'is_public': False
    })
    assert channel2.status_code == 200
    channel_id = json.loads(channel2.text)['channel_id']

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': user2_token,
        'channel_id': channel_id
    })
    assert channel_details.status_code == 200

# Change more then 2 users names in a dm
def test_user_set_name_valid_dm_2_members(register_user1, register_user2, user1_dm_id):

    token1 = register_user1['token']
    token2 = register_user2['token']

    # User 1 cerates a dm with user 2
    dm_id1 = user1_dm_id

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
    assert name1.status_code == 200

    # User 2 changes name
    name2 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token2,
        'name_first': 'good',
        'name_last': 'luck'
    })
    assert name2.status_code == 200

# Make creator of dm leave and change creators name
def test_user_set_name_valid_onwer_left(register_user1, register_user2, user1_dm_id):

    token1 = register_user1['token']
    token2 = register_user2['token']

    # User 1 cerates a dm with user 2
    dm_id1 = user1_dm_id

    # creator of dm leaves
    leave = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token1,
        'dm_id': dm_id1
    })
    assert leave.status_code == 200

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
    assert name1.status_code == 200

# Change more then 2 users names in a channel
def test_user_set_name_valid_channel_2_members(register_user1, register_user2, user1_channel_id):

    token1 = register_user1['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 creates a channel with user 2
    channel_id1 = user1_channel_id

    # user 1 invites user 2
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token1,
        'channel_id': channel_id1,
        'u_id': u_id2
    })
    assert invite.status_code == 200

    # User 1 changes name
    name1 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token1,
        'name_first': 'emily',
        'name_last': 'wong'
    })
    assert name1.status_code == 200

    # User 2 changes name
    name2 = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token2,
        'name_first': 'good',
        'name_last': 'luck'
    })
    assert name2.status_code == 200

##########################################
##### user_profile_set_email tests #######
##########################################

# Access error: invalid token
def test_user_set_email_invalid_token(register_user1):

    token = register_user1['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'aaaa123@gmail.com'
    })
    assert mail.status_code == 403

# Input Error when email entered is not a valid email
def test_user_set_email_invalid_email(register_user1):

    token = register_user1['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'abc'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': '123.com'
    })
    assert mail.status_code == 400
    assert mail1.status_code == 400

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
    assert mail2.status_code == 403
    assert mail3.status_code == 403

# Input error: email address is already being used by another user
def test_user_set_email_duplicate_email(register_user1, register_user2):

    user1_token = register_user1['token']
    user2_token = register_user2['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': user1_token,
        'email': 'elephant@gmail.com'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': user2_token,
        'email': 'cat@gmail.com'
    })
    assert mail.status_code == 400
    assert mail1.status_code == 400  

# valid case
def test_user_set_email_valid(register_user1):

    token = register_user1['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })
    assert mail.status_code == 200

# Test the user's email has been changed in a channel
def test_user_set_email_valid_channel_coverage(register_user1):
    token = register_user1['token']

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
    assert mail.status_code == 200

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': token,
        'channel_id': channel_id
    })

    member_email = json.loads(channel_details.text)['all_members'][0]['email']
    assert member_email == 'comp1531@gmail.com'
    owner_email = json.loads(channel_details.text)['owner_members'][0]['email']
    assert owner_email == member_email

# Test the user's name has been changed in a dm
def test_user_set_email_valid_dm_coverage(register_user1, user1_dm_id):
    token = register_user1['token']
    dm_id = user1_dm_id

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })
    assert mail.status_code == 200

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['email'] == 'comp1531@gmail.com'

# Change more then 2 users email in a dm
def test_user_set_email_dm_2_members(register_user1, register_user2):

    token1 = register_user1['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 cerates a dm with user 2
    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token1,
        'u_ids': [u_id2]
    })
    assert dm1.status_code == 200

    # User 1 changes email
    email1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'pain@gmail.com'
    })
    assert email1.status_code == 200

    # User 2 changes email
    email2 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token2,
        'email': 'whyyyyy@gmail.com'
    })
    assert email2.status_code == 200

# Make creator of dm leave and change creators email
def test_user_set_email_valid_onwer_left(register_user1, user1_dm_id):

    token1 = register_user1['token']

    # User 1 cerates a dm with user 2
    dm_id1 = user1_dm_id

    # creator of dm leaves
    leave = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token1,
        'dm_id': dm_id1
    })
    assert leave.status_code == 200

    # the creator of the dm who left changes email
    email1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'pain@gmail.com'
    })
    assert email1.status_code == 200

# Change more then 2 users email in a channel
def test_user_set_email_valid_channel_2_members(register_user1, register_user2, user1_channel_id):

    token1 = register_user1['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 creates a channel with user 2
    channel_id1 = user1_channel_id

    # user 1 invites user 2
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token1,
        'channel_id': channel_id1,
        'u_id': u_id2
    })
    assert invite.status_code == 200

    # user 1 chnages email
    email1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'pain@gmail.com'
    })
    assert email1.status_code == 200
    
    # user 2 changes email
    email2 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token2,
        'email': 'whyyyyy@gmail.com'
    })
    assert email2.status_code == 200

##########################################
##### user_profile_set_handle tests ######
##########################################

# Access Error: invalid token
def test_user_set_handle_invalid_token(register_user1):

    token = register_user1['token']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'ohno'
    })
    assert handle.status_code == 403

# Input error: length of handle_str is not between 3 and 20 characters inclusive
def test_user_set_handle_invalid_length(register_user1):

    token = register_user1['token']
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a1'
    })

    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a' * 22
    })
    assert handle.status_code == 400
    assert handle1.status_code == 400

    # Access Error: invalid token and invalid handle length
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a1'
    })
    assert handle2.status_code == 403

    handle3 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'a' * 22
    })
    assert handle3.status_code == 403

# Input error: handle_str contains characters that are not alphanumeric
def test_user_set_handle_non_alphanumeric(register_user1):
    
    token = register_user1['token']
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__++'
    })
    assert handle.status_code == 400

    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__:  '
    })
    assert handle.status_code == 400

    # Access Error: invalid token and invalid characters
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '__ad31__++'
    })

    handle3 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': ' ___ad31__:'
    })
    assert handle2.status_code == 403
    assert handle3.status_code == 403

# valid case
def test_user_set_handle(register_user1, register_user2, user1_dm_id, user1_channel_id):

    user1_token = register_user1['token']
    user2_token = register_user2['token']
    
    channel_id = user1_channel_id

    dm_id = user1_dm_id
    
    # valid case
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user1_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 200

    channel_details = requests.get(config.url + "channel/details/v2", params = {
        'token': user1_token,
        'channel_id': channel_id
    })
    member_handle = json.loads(channel_details.text)['all_members'][0]['handle_str']
    assert member_handle == 'anna'
    owner_handle = json.loads(channel_details.text)['all_members'][0]['handle_str']
    assert owner_handle == member_handle

    dm_details = requests.get(config.url + "dm/details/v1", params = { 
        'token': user1_token,
        'dm_id':  dm_id
    })
    assert json.loads(dm_details.text)['members'][0]['handle_str'] == 'anna'

    # the handle is already used by another user
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user2_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 400

# Change more then 2 users handle in a dm
def test_user_set_handle_dm_2_members(register_user1, register_user2):

    token1 = register_user1['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 cerates a dm with user 2
    dm1 = requests.post(config.url + "dm/create/v1", json = { 
        'token': token1,
        'u_ids': [u_id2]
    })
    assert dm1.status_code == 200

    # User 1 changes handle
    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'paiiiin'
    })
    assert handle1.status_code == 200

    # User 2 changes handle
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token2,
        'handle_str': 'wwhyyyy'
    })
    assert handle2.status_code == 200

# Make creator of dm leave and change creators name
def test_user_set_handle_valid_onwer_left(register_user1, user1_dm_id):

    token1 = register_user1['token']

    # User 1 cerates a dm with user 2
    dm_id1 = user1_dm_id

    # creator of dm leaves
    leave = requests.post(config.url + "dm/leave/v1", json = { 
        'token': token1,
        'dm_id': dm_id1
    })
    assert leave.status_code == 200

    # the creator of the dm who left changes handle
    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'paiin'
    })
    assert handle1.status_code == 200

# Change more then 2 users handle in a channel
def test_user_set_handle_valid_channel_2_members(register_user1, register_user2, user1_channel_id):

    token1 = register_user1['token']
    token2 = register_user2['token']
    u_id2 = register_user2['auth_user_id']

    # User 1 creates a channel with user 2
    channel_id1 = user1_channel_id

    # user 1 invites user 2
    invite = requests.post(config.url + "channel/invite/v2", json ={
        'token': token1,
        'channel_id': channel_id1,
        'u_id': u_id2
    })
    assert invite.status_code == 200

    # user 1 chnages email
    handle1 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'paiiin'
    })
    assert handle1.status_code == 200
    
    # user 2 changes email
    handle2 = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token2,
        'handle_str': 'whyy'
    })
    assert handle2.status_code == 200
