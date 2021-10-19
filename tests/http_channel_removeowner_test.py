import pytest
import requests
import json
from src import config 

@pytest.fixture
def register_user():

    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })
    user_data = user.json()
    return user_data

@pytest.fixture
def register_user1():

    user1 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'sally',
        'name_last': 'li'
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
###### channel_removeowner tests #########
##########################################

# access error: invalid token
def test_removeowner_invalid_token(register_user, register_user1, create_channel):
    invalid_token = register_user['token'] + 'hgjdasfi3'
    channel_id = create_channel
    user2_id = register_user1['auth_user_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': invalid_token,
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert remove.status_code == 403

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': '',
        'channel_id': channel_id,
        'u_id': user2_id
    })
    assert remove.status_code == 403

# invalid channel_id
def test_removeowner_invalid_channel_id(register_user, register_user1):

    user_token = register_user['token']
    user2_id = register_user1['auth_user_id']

    # invalid channel_id
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user_token,
        'channel_id': -1,
        'u_id': user2_id
    })
    assert remove.status_code == 400

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user_token,
        'channel_id': -256,
        'u_id': user2_id
    })
    assert remove1.status_code == 400

    # access error when invalid channel_id and invalid token
    invalid_token = register_user['token'] + 'hgjdasfi3'
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': invalid_token,
        'channel_id': -256,
        'u_id': user2_id
    })
    assert remove3.status_code == 403

# invalid u_id
def test_removeowner_invalid_u_id(register_user, register_user1, create_channel):

    user1_token = register_user['token']
    user1_channel = create_channel['channel_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': -16
    })
    assert remove.status_code == 400

    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': 'abc'
    })
    assert remove1.status_code == 400

    # invite user2 to the the channel
    user2_token = register_user1['token']
    user2_id = register_user1['auth_user_id']
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })

    # access error when invalid u_id and no owner permission
    remove2 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': -100
    })
    assert remove2.status_code == 403

    remove4 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': 'abc'
    })
    assert remove4.status_code == 403

    # access error when invalid token and invalid u_id
    invalid_token = register_user['token'] + 'hgjdasfi3'
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': invalid_token,
        'channel_id': user1_channel,
        'u_id': -16
    })
    assert remove3.status_code == 403

# u_id refers to a user who is not an owner of the channel
def test_removeowner_invalid_owner_u_id(register_user, register_user1, create_channel):

    user1_token = register_user['token']
    user1_channel = create_channel['channel_id']

    user2_token = register_user1['token']
    user2_id = register_user1['auth_user_id']

    # invite user2 to the channel
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert invite.status_code == 200

    # input error for u_id is not an owner
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove.status_code == 400

    # access error when u_id is not an owner and token has no owner permission
    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove1.status_code == 403

    # access error when invalid token and u_id is not an owner
    invalid_token = register_user['token'] + 'hgjdasfi3'
    remove3 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': invalid_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove3.status_code == 403

# u_id refers to a user who is currently the only owner of the channel
def test_removeowner_only_owner(register_user, register_user1, create_channel):

    user1_token = register_user['token']
    user1_id = register_user['auth_user_id']
    user1_channel = create_channel['channel_id']

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user1_id
    })
    assert remove.status_code == 400

    # access error when u_id is the only owner and token has no owner permission
    user2_token = register_user1['token']
    remove1 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user2_token,
        'channel_id': user1_channel,
        'u_id': user1_id
    })
    assert remove1.status_code == 403

    # access error when invalid token and u_id is not an owner
    invalid_token = register_user['token'] + 'hgjdasfi3'
    remove2 = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': invalid_token,
        'channel_id': user1_channel,
        'u_id': user1_id
    })
    assert remove2.status_code == 403

# channel_id is valid and the authorised user does not have owner permissions in the channel
def test_removeowener_no_permission(register_user, register_user1, create_channel):

    user1_token = register_user['token']
    user1_channel = create_channel['channel_id']

    user2_id = register_user1['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", json ={
        'email': 'elephant@gmail.com',
        'password': 'password',
        'name_first': 'kelly',
        'name_last': 'huang'
    })
    user3_data = user3.json()
    user3_id = user3_data['auth_user_id']
    user3_token = user3_data['token']

    # invite user1 and user2 to join the channel as a member
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user3_id
    })

    # add user2 to be an owner
    add = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert add.status_code == 200

    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user3_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove.status_code == 403

# valid case
def test_remove_owner_valid(register_user, register_user1, create_channel):

    user1_token = register_user['token']
    user1_channel = create_channel['channel_id']

    user2_id = register_user1['auth_user_id']

    # invite user2 to join the channel as a member
    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert invite.status_code == 200

    # promote user2
    add = requests.post(config.url + "channel/addowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert add.status_code == 200

    # now it should have 2 owners in the channel
    details = requests.get(config.url + "channel/details/v2", params ={
        'token': user1_token,
        'channel_id': user1_channel
    })
    owner = json.loads(details.text)['owner_members']
    assert len(owner) == 2

    # remove id2
    remove = requests.post(config.url + "channel/removeowner/v1", json ={
        'token': user1_token,
        'channel_id': user1_channel,
        'u_id': user2_id
    })
    assert remove.status_code == 200
    # only 1 owner in the channel
    details1 = requests.get(config.url + "channel/details/v2", params ={
        'token': user1_token,
        'channel_id': user1_channel
    })
    owner = json.loads(details1.text)['owner_members']
    assert len(owner) == 1
