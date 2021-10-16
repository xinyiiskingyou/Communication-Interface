import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.dm import dm_details_v1, dm_create_v1, dm_leave_v1, dm_messages_v1
from src.auth import auth_register_v2
from src.error import AccessError, InputError

NUM_MESSAGE_EXACT = 50
NUM_MESSAGE_MORE = 100
NUM_MESSAGE_LESS = 25


##########################################
#########   Dm details tests    ##########
##########################################


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
#         dm_messages_v1('asjasd','12', 0)

def test_dm_messages_error_dm_id(): 
    clear_v1()
    id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError): 
        dm_messages_v1(id1['token'], 'jasjdlak', 0)

#####HTTP######



def test_dm_message_valid_start0 (): 
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
            'email': '1531camel@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'alast'
        })

    u_id2 = json.loads(user2.text)['auth_user_id']


    dm1 = requests.post(config.url + "dm/create/v1", 
        json = { 
            'token': user1_token, 
            'u_ids': [u_id2]
        })
    dm_id1 = json.loads(dm1.text)['dm_id']

    for x in range(NUM_MESSAGE_MORE): 
        requests.post(config.url + "message/senddm/v1",
        json = {
            'token': user1_token,
            'dm_id': dm_id1,
            'message': f'hi{x}'
        })
    
    message = requests.get(config.url + "dm/messages/v1",
        params = { 
            'token': user1_token,
            'dm_id': dm_id1, 
            'start': 0 
        })
    
    message_start = json.loads(message.text)['start']
    message_end = json.loads(message.text)['end']
    assert message_start == 0 
    assert message_end == 50 
    assert len(json.loads(message.text)['messages']) == NUM_MESSAGE_EXACT

    assert message.status_code == 200 



##########################################
#########   Dm leave tests      ##########
##########################################

def test_error_leave_dmid(): 
    clear_v1()
    id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError): 
        dm_leave_v1(id1['token'], '123')

    
def test_dm_leave_valid (): 
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    dm1 = dm_create_v1(id2['token'], [id1['auth_user_id']])
    

    dm_leave_v1(id1['token'], dm1['dm_id'])


    dmdetails1 = dm_details_v1(id2['token'], dm1['dm_id'])
    assert len(dmdetails1['members']) == 1

def test_leave_invalid_dm_id(): 
    requests.delete(config.url + "clear/v1")
    creator = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })
    token = json.loads(creator.text)['token']
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abcd@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']
    u_id2 = json.loads(user1.text)['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", 
        json = { 
            'token': token, 
            'u_ids': [u_id2]
        })

    resp1 = requests.post(config.url + "dm/leave/v1", 
        json = {
            'token': token,
            'dm_id': -1
        })
    assert resp1.status_code == 400
    

def test_leave_http_valid(): 
    requests.delete(config.url + "clear/v1")

    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'email@gmail.com',
            'password': 'password',
            'name_first': 'john',
            'name_last': 'doe'
        })
    token1 = json.loads(user1.text)['token']
    token2 = json.loads(user2.text)['token']
    u_id2 = json.loads(user2.text)['auth_user_id']

    dm1 = requests.post(config.url + "dm/create/v1", 
        json = { 
            'token': token1, 
            'u_ids': [u_id2]
        })
    dm_id1 = json.loads(dm1.text)['dm_id']

    respo = requests.post(config.url + "dm/leave/v1",
        json = { 
        'token': token2, 
        'dm_id': dm_id1,
        })  
    
    assert respo.status_code == 200