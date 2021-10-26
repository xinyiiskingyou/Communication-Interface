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

# user 1 creates a channel
@pytest.fixture
def create_public_channel(register_user):

    channel = requests.post(config.url + "channels/create/v2", json ={
        'token': register_user['token'],
        'name': 'channel1',
        'is_public': True
    })
    channel_data = channel.json()
    return channel_data

##########################################
########## channel_details tests #########
##########################################

# Access error when token is not valid
def test_details_invalid_token(register_user, create_public_channel):

    token = register_user['token']
    channel = create_public_channel['channel_id']
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })

    resp1 = requests.get(config.url + "channel/details/v2", params ={
        'token': token,
        'channel_id': channel
    })
    assert resp1.status_code == 403

# Input error when channel_id is not valid
def test_details_invalid_channel_id_h(register_user):

    token1 = register_user['token']

    # Test invalid channel_id
    resp1 = requests.get(config.url + "channel/details/v2", params = {
        'token': token1,
        'channel_id': -1
    })

    resp2 = requests.get(config.url + "channel/details/v2", params = {
        'token': token1,
        'channel_id': 0
    })

    resp3 = requests.get(config.url + "channel/details/v2", params = {
        'token': token1,
        'channel_id': 256
    })

    assert resp1.status_code == 400
    assert resp2.status_code == 400
    assert resp3.status_code == 400

    # access error: invalid token and invalid channel_id
    requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    resp1 = requests.get(config.url + "channel/details/v2", params ={
        'token': token1,
        'channel_id': 256
    })
    assert resp1.status_code == 403

# Access error when the person is not a member of the channel they want details from 
def test_deatils_not_member_h(register_user1, create_public_channel):

    channel_id = create_public_channel['channel_id']

    # register user2 to not be a member of the channel
    token2 = register_user1['token']

    resp1 = requests.get(config.url + "channel/details/v2", params = {
        'token': token2,
        'channel_id': channel_id
    })
    assert resp1.status_code == 403

##### Implementation #####

# Check details for public channel
def test_details_return_values_pub_h(register_user, create_public_channel):

    token1 = register_user['token']
    u_id = register_user['auth_user_id']
    channel_id1 = create_public_channel['channel_id']
    assert channel_id1 > 0

    # Get details of channel
    resp1 = requests.get(config.url + "channel/details/v2", params ={
        'token': token1,
        'channel_id': channel_id1
    })

    assert (json.loads(resp1.text) == 
        {
        'name': 'channel1',
        'is_public': True,
        'owner_members':[
            {
                'u_id': int(u_id),
                'email': 'abcdef@gmail.com',
                'name_first': 'anna',
                'name_last': 'lee',
                'handle_str': 'annalee'
            }
        ],
        'all_members': [
            {
                'u_id': int(u_id),
                'email': 'abcdef@gmail.com',
                'name_first': 'anna',
                'name_last': 'lee',
                'handle_str': 'annalee'
            }
        ]
    })
    assert resp1.status_code == 200

# Check details for private channel
def test_details_return_values_priv_h(register_user):

    token1 = register_user['token']
    u_id = register_user['auth_user_id']
    channel1 = requests.post(config.url + "channels/create/v2", json ={
        'token': token1,
        'name': 'channel1',
        'is_public': False
    })

    channel_id1 = json.loads(channel1.text)['channel_id']
    assert channel_id1 == json.loads(channel1.text)['channel_id']

    # Get details of channel
    resp1 = requests.get(config.url + "channel/details/v2", params ={
        'token': token1,
        'channel_id': json.loads(channel1.text)['channel_id'],
    })

    assert (json.loads(resp1.text) == 
        {
        'name': 'channel1',
        'is_public': False,
        'owner_members':[
            {
                'u_id': int(u_id),
                'email': 'abcdef@gmail.com',
                'name_first': 'anna',
                'name_last': 'lee',
                'handle_str': 'annalee'
            }
        ],
        'all_members': [
            {
                'u_id': int(u_id),
                'email': 'abcdef@gmail.com',
                'name_first': 'anna',
                'name_last': 'lee',
                'handle_str': 'annalee'
            }
        ]
    })
    assert resp1.status_code == 200

# Check details for when someone is invited to the channel
def test_details_return_values_invite_h(register_user, register_user1, create_public_channel):

    # User 1 creates a channel
    token1 = register_user['token']
    
    # create an user 2
    u_id = register_user1['auth_user_id']

    # User 1 invites user 2 to the channel they created
    channel_id1 = create_public_channel['channel_id']
    invite2 = requests.post(config.url + "channel/invite/v2", json ={
        'token': token1,
        'channel_id': channel_id1,
        'u_id': u_id
    })

    assert invite2.status_code == 200

    # Get details of channel
    resp1 = requests.get(config.url + "channel/details/v2", params ={
        'token': token1,
        'channel_id': channel_id1
    })
    assert resp1.status_code == 200

    # Check length of members list 
    members = json.loads(resp1.text)['owner_members']
    assert len(members) == 1
    members = json.loads(resp1.text)['all_members']
    assert len(members) == 2
