import pytest
import requests
import json
from src import config 

@pytest.fixture
def register_user():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'afirst',
        'name_last': 'alast'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user1():
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcertgh@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
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
######### channel_addowner tests #########
##########################################

# Access error: invalid token
def test_addowner_invalid_token(register_user, register_user1, create_channel):
    invalid_token = register_user['token'] +'dskfjoiie'
    channel_id = create_channel['channel_id']
    u_id = register_user1['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': invalid_token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == 403

    resp2 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': '',
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp2.status_code == 403

# Input error: invalid channel_id
def test_invalid_channel_id(register_user, register_user1):

    token = register_user['token']
    u_id = register_user1['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 123,
        'u_id': u_id
    })

    resp2 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': '123',
        'u_id': u_id
    })
    assert resp1.status_code == 400
    assert resp2.status_code == 400

    # access error: invalid token and invalid channel_id
    invalid_token = register_user['token'] +'dskfjoiie'
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': invalid_token,
        'channel_id': 123,
        'u_id': u_id
    })
    assert resp3.status_code == 403

 # invalid u_id
def test_invalid_u_id(register_user, register_user1, create_channel):

    token = register_user['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': -1
    })
    assert resp1.status_code == 400

    # access error: invalid token and invalid u_id
    invalid_token = register_user['token'] +'dskfjoiie'
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': invalid_token,
        'channel_id': channel_id,
        'u_id': -1
    })
    assert resp3.status_code == 403

    # access error: invalid u_id and token has no owner permission
    token2 = register_user1['token']
    u_id1 = register_user1['auth_user_id']
    # invite user2 to join the channel
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id1
    })
    
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': -1
    })

    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': 123
    })
    assert resp1.status_code == 403
    assert resp2.status_code == 403

# u_id not a member of the channel
def test_not_member_u_id(register_user, register_user1, create_channel):

    token = register_user['token']
    channel_id = create_channel['channel_id']

    u_id = register_user1['auth_user_id']
    token2 = register_user1['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == 400

    # access error: invalid token and u_id is not a member of the channel
    invalid_token = register_user['token'] +'dskfjoiie'
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': invalid_token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp3.status_code == 403

    # access error: token has no owner permission and u_id is not a member
    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp2.status_code == 403

# u_id already owner of the channel
def test_already_owner(register_user, register_user1, create_channel):

    token = register_user['token']
    u_id = register_user['auth_user_id']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == 400

    # add user2 to be the owner of the channel
    u_id2 = register_user1['auth_user_id']
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert invite.status_code == 200

    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert resp2.status_code == 200

    # raise error since user2 is already the owner of the channel
    resp3 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert resp3.status_code == 400

    # invite id3 to the channel
    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    token3 = json.loads(id3.text)['token']
    u_id3 = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id3
    })
    # access error: token has no owner permission and u_id is already an owner
    resp4 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token3,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert resp4.status_code == 403

# No owner permission
def test_no_perm_not_member(register_user, register_user1, create_channel):

    token1 = register_user['token']
    channel_id = create_channel['channel_id']

    u_id1 = register_user1['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id1
    })

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    # user3 is not able to add id2 to be the owner
    token2 = json.loads(id3.text)['token']
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id1
    })
    assert resp1.status_code == 403

def test_no_perm_not_owner(register_user, create_channel, register_user1):

    token1 = register_user['token']
    channel_id = create_channel['channel_id']

    token2 = register_user1['token']
    u_id1 = register_user1['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
        })
    u_id2 = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id1
    })
    
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    })

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id2
    })
    assert resp1.status_code == 403

# valid case
def test_valid_addowner(register_user, register_user1, create_channel):

    token = register_user['token']
    channel_id = create_channel['channel_id']

    u_id = register_user1['auth_user_id']
    
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert resp1.status_code == 200

def test_addowner_valid_global(register_user, register_user1):

    token = register_user['token']

    # user 2 (not global owner) creates a channel
    token2 = register_user1['token']
    ch1 = requests.post(config.url + "channels/create/v2", json = {
        'token': token2,
        'name': '1531_CAMEl',
        'is_public': True
    })
    channel_id = json.loads(ch1.text)['channel_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'hellokitty@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'kitty'
        })
    u_id = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id
    })

    # token1 can add id3 to be an owner since token1 is a global owner
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })

    assert resp1.status_code == 200
