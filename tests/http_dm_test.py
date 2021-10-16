import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.dm import dm_details_v1, dm_create_v1
from src.auth import auth_register_v2
from src.error import AccessError, InputError



##########################################
#########   Dm details tests    ##########
##########################################

# def test_dm_details_error_token(): 
#     clear_v1()
#     with pytest.raises(InputError):
#         dm_details_v1('','123')

def test_dm_details_error_dm_id(): 
    clear_v1()
    id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError): 
        dm_details_v1(id1['token'], '123')

##add valid tests 

def test_dm_details_valid(): 
    clear_v1()
    id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('kjhd1@gmail.com', 'pass123', 'ashley', 'wong')
    dm1 = dm_create_v1(id1['token'], [id2['auth_user_id']])
    dm_details = dm_details_v1(id1['token'], dm1['dm_id'])

    assert len(dm_details['members']) == 2



##### HTTP #####
def test_http_dm_details_valid(): 
    requests.delete(config.url + "clear/v1")

    user1 = requests.post(config.url + "auth/register/v2",
        json = { 
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token = json.loads(user1.text)['token']
    user2 = requests.post(config.url + "auth/register/v2", 
        json = { 
            'email': 'email@gmail.com',
            'password': 'password',
            'name_first': 'john',
            'name_last': 'doe'
        })
    token2 = json.loads(user2.text)['token']
    u_id2 = json.loads(user2.text)['auth_user_id']


    dm1 = requests.post(config.url + "dm/create/v1",
        json = { 
            'token': token,
            'u_ids': [u_id2]
        })
    dm_id = json.loads(dm1.text)['dm_id']
    resp1 = requests.get(config.url + "dm/details/v1", 
        params = { 
            'token': token2,
            'dm_id':  dm_id
        })
    assert resp1.status_code == 200 

    
##########################################
#########   Dm messages tests   ##########
##########################################

# def test_dm_messages_error_token(): 
#     clear_v1()
#     with pytest.raises(InputError):
#         dm_messages_v1('asjasd','', 5)

# def test_dm_messages_error_dm_id(): 
#     clear_v1
#     id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
#     with pytest.raises(InputError): 
#         dm_messages_v1(id1['token'], 'jasjdlak', 5)


##########################################
########### message/senddm/v1 ############
##########################################
# Input Error when channel_id does not refer to a valid channel
# when dm_id is negative
def test_dm_send_invalid_channel_id_positive():
    requests.delete(config.url + "clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    send_dm = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': -2, 
            'message': 'hello there'
        }
    )
    assert send_dm.status_code == 400


# Input Error when channel_id does not refer to a valid channel
# id is positive integer, but is not an id to any channel
def test_dm_send_invalid_dm_id_nonexistant():
    requests.delete(config.url + "clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']
   

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_id = json.loads(user2.text)['auth_user_id']

    requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    send_dm = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': 256, 
            'message': 'hello there'
        }
    )
    assert send_message.status_code == 400


# Input error when length of message is less than 1 or over 1000 characters
def test_dm_send_invalid_message():
    requests.delete(config.url + "clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_id = json.loads(user2.text)['auth_user_id']

    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(dm1.text)['dm_id']

    send_dm1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'channel_id': user2_id,
            'message': 'a' * 1001
        }
    )
    assert send_message1.status_code == 400

    send_message2 = requests.post(config.url + "message/send/v1",
        json = {
            'token': user1_token,
            'channel_id': user2_id,
            'message': ''
        }
    )
    assert send_message2.status_code == 400


# Access error when channel_id is valid and the authorised user 
# is not a member of the channel
def test_dm_send_unauthorised_user():
    requests.delete(config.url + "clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'email@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        }
    )
    user3_token = json.loads(user3.text)['token']

    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(dm1.text)['dm_id']

    send_message1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user3_token,
            'channel_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_message1.status_code == 403


##### Implementation #####

# Send message in one dm by two users
def test_dm_send_valid_two_dm_messages():
    requests.delete(config.url + "clear/v1")
    # Register user 1
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    # User 1 creates channel 1
    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(dm1.text)['dm_id']

    # User 1 sends message 1 in channel 1
    send_dm1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_message1.status_code == 200
    json.loads(send_dem1.text)['dm_id']

    # User 2 sends a message in channel 1
    send_dm2 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    json.loads(send_dm2.text)['dm_id']
    assert send_message2.status_code == 200


# Send message in one dm and compare dm message_id to 
# ensure different dm message_id's across different dm's
def test_dm_send_valid_diff_id():
    requests.delete(config.url + "clear/v1")
    # Register user 1
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    # User 1 creates channel 1
    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(dm1.text)['dm_id']

    # User 1 sends message 1 in channel 1
    send_dm1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_dm1.status_code == 200
    message_dm1 = json.loads(send_dm1.text)['dm_id']

    assert send_message1.status_code == 200
    json.loads(send_dem1.text)['dm_id']

    # User 2 sends a message in channel 1
    send_dm2 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_dm2.status_code == 200
    message_dm2 = json.loads(send_dm2.text)['dm_id']

    assert message_dm1 !=  message_dm2
