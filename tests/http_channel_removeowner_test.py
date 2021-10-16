import pytest
import requests
import json
from src import config 

# invalid channel_id
def test_removeowner_invalid_channel_id():

    requests.delete(config.url + "clear/v1")

    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    u_id = user_data['auth_user_id']
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    u_id2 = user1_data['auth_user_id']
    token2 = user1_data['token']
    
    # invalid channel_id
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': -1,
        'u_id': u_id2
    })

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': 'not_an_id',
        'u_id': u_id2
    })
    assert remove.status_code == 400
    assert remove1.status_code == 400

    # access error when invalid channel_id and no owner permission
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token2,
        'channel_id': -1,
        'u_id': u_id
    })
    assert remove3.status_code == 403

# invalid u_id
def test_removeowner_invalid_u_id():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    token = json.loads(user.text)['token']
    u_id = json.loads(user.text)['auth_user_id']

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': -16
    })

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': ''
    })
    assert remove.status_code == 400
    assert remove1.status_code == 400

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token2 = user1_data['token']

    # access error when invalid channel_id and no owner permission
    remove2 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token2,
        'channel_id': -1,
        'u_id': u_id
    })
    assert remove2.status_code == 403

# u_id refers to a user who is not an owner of the channel
def test_removeowner_invalid_owner_u_id():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    token = json.loads(user.text)['token']

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    u_id = user1_data['auth_user_id']
    token2 = user1_data['token']

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 200

    # input error for u_id is not an owner
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert remove.status_code == 400

    # access error when u_id is not an owner and token has no owner permission
    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert remove1.status_code == 403

# u_id refers to a user who is currently the only owner of the channel
def test_removeowner_only_owner():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    token = user_data['token']
    u_id = user_data['auth_user_id']

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert remove.status_code == 400

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    token2 = user1_data['token']

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert remove1.status_code == 403

# channel_id is valid and the authorised user does not have owner permissions in the channel
def test_removeowener_no_permission():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    user_data = user.json()
    token = user_data['token']

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    u_id = user1_data['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user2_data = user2.json()
    u_id2 = user2_data['auth_user_id']
    token2 = user2_data['token']

    # invite user1 and user2 to join the channel as a member
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    invite2 = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert invite.status_code == 200
    assert invite2.status_code == 200

    # add user1 to be an owner
    add = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert add.status_code == 200

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert remove.status_code == 403

# valid case
def test_remove_owner_valid():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcde@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'li'
    })
    token = json.loads(user.text)['token']

    channel = requests.post(config.url + "channels/create/v2", json = {
        'token': token,
        'name': 'anna',
        'is_public': True
    })
    channel_id = json.loads(channel.text)['channel_id']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    u_id = user1_data['auth_user_id']

    # invite user1 to join the channel as a member
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 200

    # promote user1
    add = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert add.status_code == 200

    details = requests.get(config.url + "channel/details/v2", 
        params = {
        'token': token,
        'channel_id': channel_id
    })

    members = json.loads(details.text)['owner_members']
    assert len(members) == 2

    # remove id2
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    details1 = requests.get(config.url + "channel/details/v2", 
        params = {
        'token': token,
        'channel_id': channel_id
    })
    owner = json.loads(details1.text)['owner_members']

    assert remove.status_code == 200
    assert len(owner) == 1
