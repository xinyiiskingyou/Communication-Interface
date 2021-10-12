from re import I
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
    token = user_data['token']

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
    })
    user1_data = user1.json()
    u_id = user1_data['auth_user_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': -1,
        'u_id': u_id
    })

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': 'not_an_id',
        'u_id': u_id
    })
    assert remove.status_code == 400
    assert remove1.status_code == 400

# invalid u_id
def test_removeowner_invalid_u_id():

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

# u_id refers to a user who is not an owner of the channel
def test_removeowner_invalid_owner_u_id():

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

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 200

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert remove.status_code == 400

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
    add = requests.post(config.url + "channels/addowner/v1", json = {
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

    # invite user1 to join the channel as a member
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert invite.status_code == 200

    # promote user1
    add = requests.post(config.url + "channels/addowner/v1", json = {
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
    remove = requests.post(config.url + "channels/removeowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert remove.status_code == 200
    assert len(members) == 1