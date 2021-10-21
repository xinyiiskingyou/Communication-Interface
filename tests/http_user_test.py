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

    assert (json.loads(all1.text) == 
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
    assert len(json.loads(all1.text)) == 2
    assert len(json.loads(all2.text)) == 2
    assert len(json.loads(all1.text)) == len(json.loads(all2.text))

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
    # Invalid u_id's
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

    # access error: invalid token and invalid u_id
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
    assert (json.loads(profile.text) == 
        {
        'u_id': u_id,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'lee',
        'handle_str': 'annalee'
    })

# Valid Case for looking at someone elses profile
def test_user_profile_valid_someone_else(register_user1, register_user2):

    token = register_user1['token']
    u_id2 = (register_user2['auth_user_id'])

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id2
    })

    assert profile.status_code == 200
    assert (json.loads(profile.text) == 
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
        'name_first': 'a' * 51,
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
def test_user_set_name_valid_name_first(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']

    # Valid last name
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'lee'
    })

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })
   
    assert (json.loads(profile.text) == 
    {
        'u_id': 1,
        'email': 'cat@gmail.com',
        'name_first': 'annabelle',
        'name_last': 'lee',
        'handle_str': 'annalee'
    })

    assert name.status_code == 200

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
   
    assert (json.loads(profile.text) == 
    {
        'u_id': 1,
        'email': 'cat@gmail.com',
        'name_first': 'anna',
        'name_last': 'park',
        'handle_str': 'annalee'
    })

    assert name.status_code == 200

# Valid first and last name change
def test_user_set_name_valid_name_first_and_last(register_user1):

    token = register_user1['token']
    u_id = register_user1['auth_user_id']

    # Invalid last name
    name = requests.put(config.url + "user/profile/setname/v1", json ={
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'parker'
    })

    profile = requests.get(config.url + "user/profile/v1", params ={
        'token': token,
        'u_id': u_id
    })
   
    assert (json.loads(profile.text) == 
    {
        'u_id': 1,
        'email': 'cat@gmail.com',
        'name_first': 'annabelle',
        'name_last': 'parker',
        'handle_str': 'annalee'
    })

    assert name.status_code == 200

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

    # access error: invalid token and invalid email
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


# email address is already being used by another user
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

# length of handle_str is not between 3 and 20 characters inclusive
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


# handle_str contains characters that are not alphanumeric
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

def test_user_set_handle(register_user1, register_user2):

    user1_token = register_user1['token']
    user2_token = register_user2['token']

    # valid case
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user1_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 200

    # the handle is already used by another user
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': user2_token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 400
