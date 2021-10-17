import pytest
import requests
import json
from src import config

##########################################
######## admin_user_remove tests #########
##########################################

# Input error: u_id does not refer to a valid user
def test_admin_remove_invalid_u_id():
    requests.delete(config.url + "clear/v1", json={})
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    response_data = user1.json()
    token = response_data['token']

    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': -1
    })
    
    remove1 = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': ''
    })

    assert remove.status_code == 400
    assert remove1.status_code == 400

    # access error: u_id is invalid and authorised user is not a global owner
    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']

    remove3 = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token2,
        'u_id': -1
    })

    assert remove3.status_code == 403

# u_id refers to a user who is the only global owner
def test_admin_global_owner():
    requests.delete(config.url + "clear/v1", json={})
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    response_data = user1.json()
    token = response_data['token']
    u_id = response_data['auth_user_id']

    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token,
        'u_id': u_id
    })
    assert remove.status_code == 400

# Access error: the authorised user is not a global owner
def test_admin_remove_not_global_owner():
    requests.delete(config.url + "clear/v1", json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'sally123@gmail.com', 
        'password': 'password1234', 
        'name_first': 'sally', 
        'name_last': 'wong'
    })
    response_data = user1.json()
    u_id = response_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']

    remove = requests.delete(config.url + 'admin/user/remove/v1', json ={
        'token': token2,
        'u_id': u_id
    })

    assert remove.status_code == 403

# remove stream member
def test_admin_remove_valid():

    requests.delete(config.url + "clear/v1", json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'sally123@gmail.com', 
        'password': 'password1234', 
        'name_first': 'sally', 
        'name_last': 'wong'
    })
    response_data = user1.json()
    token = response_data['token']

    # user 1 creates a channel
    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'sally',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']
    u_id = user2_data['auth_user_id']

    # invites user2 to join user1's channel
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 200

    # user 1 creates a dm 
    dm = requests.post(config.url + "dm/create/v1", json = { 
        'token': token,
        'u_ids': [u_id]
    })
    dm_data = dm.json()
    dm_id = dm_data['dm_id']
    
    # user2 sends a message
    message = requests.post(config.url + "message/send/v1", json = {
            'token': token2,
            'channel_id': channel_id,
            'message': 'hello there'
        }
    )
    assert message.status_code == 200

    # now remove user2
    remove = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': token,
        'u_id': u_id
    })
    assert remove.status_code == 200

    # id2 is removed from id1's channel
    channel_detail = requests.get(config.url + "channel/details/v2", 
        params = {
        'token': token,
        'channel_id': channel_id
    })
    assert len(json.loads(channel_detail.text)['all_members']) == 1

    # id2 is removed from id1's dm
    dm_detail = requests.get(config.url + "dm/details/v1", params = { 
        'token': token2,
        'dm_id': [dm_id]
    })
    # since id2 is not valid now
    assert dm_detail.status_code == 403

    '''
    # the contents of the messages will be replaced by 'Removed user'
    messages = requests.get(config.url + "channel/messages/v2", 
        params = {
            'token': token2,
            'channel_id': channel_id,
            'start': 0
        }
    )
    print(json.loads(messages.text))
    assert json.loads(messages.text)['messages'] == 'Removed user'
    '''

    # there are only 1 valid user in user/all now
    user_list = requests.get(config.url + "user/all/v1", params ={
        'token': token
    })
    assert len(json.loads(user_list.text)) == 1

    # the profile of removed user is still retrievable
    profile = requests.get(config.url + "user/profile/v1", 
        params = {
        'token': token,
        'u_id': u_id
    })  
    # name_first should be 'Removed' and name_last should be 'user'.
    assert profile.status_code == 200
    assert json.loads(profile.text)['name_first'] == 'Removed'
    assert json.loads(profile.text)['name_last'] == 'user'
    
    # user2's email and handle should be reusable.
    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    assert user3.status_code == 200

# Streams owners can remove other Streams owners (including the original first owner)
def test_admin_remove_valid1():

    requests.delete(config.url + "clear/v1", json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'sally123@gmail.com', 
        'password': 'password1234', 
        'name_first': 'sally', 
        'name_last': 'wong'
    })
    response_data = user1.json()
    token = response_data['token']
    u_id = response_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']
    u_id2 = user2_data['auth_user_id']

    promote = requests.post(config.url + "admin/userpermission/change/v1", json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 1
    })
    assert promote.status_code == 200

    demote = requests.delete(config.url + "admin/user/remove/v1", json ={
        'token': token2,
        'u_id': u_id
    })

    assert demote.status_code == 200

##########################################
#### admin_userpermission_change tests ###
##########################################

# u_id does not refer to a valid user
def test_admin_perm_invalid_u_id():
    requests.delete(config.url + 'clear/v1', json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    response_data = user1.json()
    token = response_data['token']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': -1,
        'permission_id': 1
    })

    perm1 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': '',
        'permission_id': 1
    })

    assert perm.status_code == 400
    assert perm1.status_code == 400

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']

    # u_id is invalid the authorised user is not a global owner
    # raise Access error in this case
    perm3 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': -1,
        'permission_id': 1
    })
    assert perm3.status_code == 403

# u_id refers to a user who is the only global owner and they are being demoted to a user
def test_admin_invalid_demote():
    requests.delete(config.url + 'clear/v1', json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    response_data = user1.json()
    token = response_data['token']
    u_id = response_data['auth_user_id']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id,
        'permission_id': 2
    })

    assert perm.status_code == 400

def test_admin_invalid_demote1():
    requests.delete(config.url + 'clear/v1', json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    response_data = user1.json()
    token = response_data['token']
    u_id = response_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']
    u_id2 = user2_data['auth_user_id']

    # id1 promotes id2
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 1
    })
    assert perm.status_code == 200

    # id2 demotes id1
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 2
    })

    # raise Input error if user2 demotes themselves 
    # since user2 is now the only global owner
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id2,
        'permission_id': 2
    })

    assert perm.status_code == 400

# permission id is invalid 
def test_admin_invalid_permission_id():
    requests.delete(config.url + 'clear/v1', json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    response_data = user1.json()
    token = response_data['token']
    u_id = response_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']
    u_id2 = user2_data['auth_user_id']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 100
    })
    assert perm.status_code == 400

    perm1 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': -100
    })
    assert perm1.status_code == 400

    # access error when permission id is invalid and the authorised user is not a global owner
    perm2 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': -100
    })
    assert perm2.status_code == 403

# the authorised user is not a global owner
def test_admin_perm_not_global_owner():
    requests.delete(config.url + 'clear/v1', json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    response_data = user1.json()
    u_id = response_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']

    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 1
    })

    assert perm.status_code == 403

# valid case
def test_valid_permission_change():
    requests.delete(config.url + 'clear/v1', json={})
    user1 = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    response_data = user1.json()
    token = response_data['token']
    u_id = response_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user2_data = user2.json()
    token2 = user2_data['token']
    u_id2 = user2_data['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'cute@unsw.edu.au',
        'password': 'password2',
        'name_first': 'tina',
        'name_last': 'huang'
    })
    user3_data = user3.json()
    token3 = user3_data['token']
    u_id3 = user3_data['auth_user_id']

    # id1 promotes id2 and id3
    perm = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id2,
        'permission_id': 1
    })
    assert perm.status_code == 200

    perm1 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token,
        'u_id': u_id3,
        'permission_id': 1
    })
    assert perm1.status_code == 200

    # now user3 has the permission to demote user1(the original owner)
    perm2 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token3,
        'u_id': u_id,
        'permission_id': 2
    })
    assert perm2.status_code == 200

    # user2 also has the permission to promote user1 back
    perm3 = requests.post(config.url + 'admin/userpermission/change/v1', json ={
        'token': token2,
        'u_id': u_id,
        'permission_id': 1
    })
    assert perm3.status_code == 200
