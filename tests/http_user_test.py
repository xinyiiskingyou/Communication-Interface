import pytest
import requests
import json
from src import config 

##########################################
############ users_all tests ##############
##########################################

# Valid case when there is only 1 user
def test_user_all_1_member():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    mail1 = requests.get(config.url + "user/all/v1", 
        json = {
        'token': token
    })

    assert (json.loads(mail1.text) == 
    [{
        'u_id': 1,
        'email': 'abcdef@gmail.com',
        'name_first': 'anna',
        'name_last': 'lee',
        'handle_str': 'annalee'
    }])
    assert len(json.loads(mail1.text)) == 1


# Valid case when there is more then 1 user
def test_user_all_several_members():
    requests.delete(config.url + "clear/v1", json={})

    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'email@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user2.json()
    token = user_data['token']

    mail1 = requests.get(config.url + "user/all/v1", 
        json = {
        'token': token
    })

    # test using length of list as cannot be certain 
    # the listed order of users
    members = json.loads(mail1.text)
    assert len(members) == 2


##########################################
########## user_profile tests ############
##########################################

# Input error for invalid u_id
def test_user_profile_invalid_u_id():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    # Invalid u_id's
    mail1 = requests.get(config.url + "user/profile/v1", 
        params = {
        'token': token,
        'u_id': -1
    })

    ''' 
   mail2 = requests.get(config.url + "user/profile/v1", 
        params = {
        'token': token,
        'u_id': 0
    })

    mail3 = requests.get(config.url + "user/profile/v1", 
        params = {
        'token': token,
        'u_id': 256
    })
    '''

    assert mail1.status_code == 400
    #assert mail2.status_code == 400
    #assert mail3.status_code == 400


##### Implementation #####

# Valid Case for looking at own profile
def test_user_profile_valid_own():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    user_data = user.json()
    token = user_data['token']
    u_id = (user_data['auth_user_id'])

    mail = requests.get(config.url + "user/profile/v1", 
        params = {
        'token': token,
        'u_id': u_id
    })

    assert mail.status_code == 200
    assert (json.loads(mail.text) == 
        {
        'user_id': u_id,
        'email': 'abc@gmail.com',
        'name_first': 'anna',
        'name_last': 'park',
        'handle_str': 'annapark'
    })


# Valid Case for looking at someone elses profile
def test_user_profile_valid_someone_else():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'john',
        'name_last': 'park'
    })

    user_data = user.json()
    token = user_data['token']

    user_data2 = user2.json()
    u_id2 = (user_data2['auth_user_id'])

    mail = requests.get(config.url + "user/profile/v1", 
        params = {
        'token': token,
        'u_id': u_id2
    })

    assert mail.status_code == 200
    assert (json.loads(mail.text) == 
        {
        'user_id': u_id2,
        'email': 'abcdef@gmail.com',
        'name_first': 'john',
        'name_last': 'park',
        'handle_str': 'johnpark'
    })


##########################################
###### user_profile_set_name tests #######
##########################################

# Input error when length of first name is < 1 or > 50

def test_user_name_invalid_name_first():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    # Invalid first name
    mail = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': '',
        'name_last': 'lee'
    })

    mail1 = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': 'a' * 51,
        'name_last': 'lee'
    })

    assert mail.status_code == 400
    assert mail1.status_code == 400


# Input error when length of first name is < 1 or > 50
def test_user_set_name_invalid_name_last():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    
    user_data = user.json()
    token = user_data['token']

    # Invalid last name
    mail = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': 'anna',
        'name_last': ''
    })

    mail1 = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': 'anna',
        'name_last': 'a' * 51
    })

    assert mail.status_code == 400
    assert mail1.status_code == 400

##### Implementation #####

# Valid first name change 
def test_user_set_name_valid_name_first():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    # Valid last name
    mail = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'lee'
    })

    assert mail.status_code == 200

# Valid last name change
def test_user_set_name_valid_name_last():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    # Valid last name
    mail = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': 'anna',
        'name_last': 'parker'
    })

    assert mail.status_code == 200

# Valid first and last name change
def test_user_set_name_valid_name_first_and_last():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    # Invalid last name
    mail = requests.put(config.url + "user/profile/setname/v1", 
        json = {
        'token': token,
        'name_first': 'annabelle',
        'name_last': 'parker'
    })

    assert mail.status_code == 200


##########################################
##### user_profile_set_email tests #######
##########################################

# Input Error when email entered is not a valid email
def test_user_set_email_invalid_email():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

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

# email address is already being used by another user
def test_user_set_email_duplicate_email():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cat@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token1 = user1_data['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'elephant@gmail.com'
    })

    mail1 = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token1,
        'email': 'cat@gmail.com'
    })
    assert mail.status_code == 400
    assert mail1.status_code == 400  

# valid case
def test_user_set_email_valid():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cat@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    mail = requests.put(config.url + "user/profile/setemail/v1", json ={
        'token': token,
        'email': 'comp1531@gmail.com'
    })

    assert mail.status_code == 200

##########################################
##### user_profile_set_handle tests ######
##########################################

# length of handle_str is not between 3 and 20 characters inclusive
def test_user_set_handle_invalid_length():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

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

# handle_str contains characters that are not alphanumeric
def test_user_set_handle_non_alphanumeric():
    
    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': '___ad31__++'
    })
    assert handle.status_code == 400

def test_user_set_handle():

    requests.delete(config.url + "clear/v1", json={})
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token1 = user1_data['token']

    # valid case
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token,
        'handle_str': 'anna'
    })
    assert handle.status_code == 200

    # the handle is already used by another user
    handle = requests.put(config.url + "user/profile/sethandle/v1", json ={
        'token': token1,
        'handle_str': 'anna'
    })
    assert handle.status_code == 400
