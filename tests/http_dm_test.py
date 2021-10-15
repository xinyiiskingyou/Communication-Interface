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

