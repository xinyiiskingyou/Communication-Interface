import pytest
import requests
import json
from src import config 

@pytest.fixture
def register_user1():

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
def register_user2():
    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcertgh@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user1_data = user1.json()
    return user1_data

# user 1 creates a channel
@pytest.fixture
def create_channel(register_user1):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user1['token'],
        'name': 'anna',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data

##########################################
######### channel_addowner tests #########
##########################################

# Access error: invalid token
def test_addowner_invalid_token(register_user1, register_user2, create_channel):
    token = register_user1['token']
    channel_id = create_channel['channel_id']
    u_id = register_user2['auth_user_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    })
    assert resp1.status_code == 403

# Input error: invalid channel_id
def test_invalid_channel_id(register_user1, register_user2):

    token = register_user1['token']
    u_id = register_user2['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 123,
        'u_id': u_id
    })

    resp2 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 'abc',
        'u_id': u_id
    })
    assert resp1.status_code == 400
    assert resp2.status_code == 400

    # Access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': 123,
        'u_id': u_id
    })
    assert resp3.status_code == 403

 # Input error: invalid u_id
def test_invalid_u_id(register_user1, register_user2, create_channel):

    token = register_user1['token']
    channel_id = create_channel['channel_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': -1
    })
    assert resp1.status_code == 400

    # Access error: invalid u_id and token has no owner permission
    token2 = register_user2['token']
    u_id1 = register_user2['auth_user_id']

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

    # Access error: invalid token and invalid u_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': -1
    })
    assert resp3.status_code == 403

# Input error: u_id not a member of the channel
def test_not_member_u_id(register_user1, register_user2, create_channel):

    # user1 creates a channel
    user1_token = register_user1['token']
    channel_id = create_channel['channel_id']

    # register user2 to not be a member of the channel
    user2_id = register_user2['auth_user_id']
    user2_token = register_user2['token']

    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp1.status_code == 400

    # Access error: token has no owner permission and u_id is not a member
    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp2.status_code == 403 

    # Access error: invalid token and u_id is not a member of the channel
    requests.post(config.url + "auth/logout/v1", json = {
        'token': user1_token
    })
    resp3 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp3.status_code == 403

# Input error: u_id refers to the user who is already owner of the channel
def test_already_owner(register_user1, register_user2, create_channel):

    # user1 creates a channel
    user1_token = register_user1['token']
    user1_id = register_user1['auth_user_id']
    channel_id = create_channel['channel_id']

    # raise error as user1 is already the owner
    resp1 = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })
    assert resp1.status_code == 400

    # add user2 to be the owner of the channel
    user2_id = register_user2['auth_user_id']
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert invite.status_code == 200

    resp2 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp2.status_code == 200

    # raise error since user2 is already the owner of the channel
    resp3 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp3.status_code == 400

    # invite id3 to the channel
    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user3_token = json.loads(id3.text)['token']
    user3_id = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    # access error: token has no owner permission and u_id is already an owner
    resp4 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user3_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp4.status_code == 403

# Access error: channel_id is valid and the authorised user does not 
# have owner permissions in the channel
def test_no_perm_not_member(register_user1, register_user2, create_channel):

    # user 1 creates a channel
    user1_token = register_user1['token']
    channel_id = create_channel['channel_id']

    # invite user2 to the channel
    user2_id = register_user2['auth_user_id']
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })

    # register user3 to not be in the channel
    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user3_token = json.loads(id3.text)['token']

    # user3 is not able to add id2 to be the owner as user3 is not 
    # a member of the channel
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user3_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert resp1.status_code == 403

# more test for access error
def test_no_perm_not_owner(register_user1, create_channel, register_user2):

    # user1 creates a channel
    user1_token = register_user1['token']
    channel_id = create_channel['channel_id']

    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'apple@gmail.com',
        'password': 'password',
        'name_first': 'hello',
        'name_last': 'world'
    })
    user3_id = json.loads(id3.text)['auth_user_id']

    # invite both user2 and user3 to the channel
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })

    # user2 is not able to add id3 to the channel 
    # as user2 does not have owener permission
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    assert resp1.status_code == 403

##### Implementation ######

# valid case
def test_valid_addowner(register_user1, register_user2, create_channel):

    # user1 creates a channel
    token = register_user1['token']
    channel_id = create_channel['channel_id']

    # register user2
    user2_id = register_user2['auth_user_id']
    
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': channel_id,
        'u_id': user2_id
    })

    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': token,
        'channel_id': channel_id,
        'u_id': user2_id
    })

    assert resp1.status_code == 200

# test valid case when global owner can add owner in the channel
def test_addowner_valid_global(register_user1, register_user2):

    user1_token = register_user1['token']
    user1_id = register_user1['auth_user_id']

    # user 2 (not global owner) creates a channel
    user2_token = register_user2['token']
    ch1 = requests.post(config.url + "channels/create/v2", json = {
        'token': user2_token,
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
    user3_id = json.loads(id3.text)['auth_user_id']

    # invite user1 and user3 to the channel
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user1_id
    })

    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user2_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })

    # user1 can add id3 to be an owner since user1 is a global owner
    resp1 = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': channel_id,
        'u_id': user3_id
    })
    assert resp1.status_code == 200
