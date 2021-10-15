import pytest
import requests
import json
from src import config 

##########################################
######### channel_addowner tests ##########
##########################################

def test_invalid_channel_id():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(id1.text)['token']

    id2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abcertgh@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
        })

    u_id = json.loads(id2.text)['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': 123,
            'u_id': u_id
        })

    resp2 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': '123',
            'u_id': u_id
        })
    assert resp1.status_code == 400
    assert resp2.status_code == 400

def test_invalid_u_id():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(id1.text)['token']

    id2 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token,
            'name': '1531_CAMEL',
            'is_public': True
        })
    channel_id = json.loads(id2.text)['channel_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': channel_id,
            'u_id': -1
        })
    assert resp1.status_code == 400

def test_not_member_u_id():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token,
            'name': '1531_CAMEL',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']


    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
        })

    u_id = json.loads(id2.text)['auth_user_id']

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })
    assert resp1.status_code == 400

def test_already_owner():
    # TODO: figure why fail when owner invite an user and 
    # failes to add this user as owner
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token = json.loads(id1.text)['token']
    u_id = json.loads(id1.text)['auth_user_id']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    '''
    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    
    
    invite = requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })
    '''
    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })
    '''
    resp2 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })
        '''
    assert resp1.status_code == 400

def test_no_perm_not_member():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token1 = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token1,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    u_id1 = json.loads(id2.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })

    id3 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'apple@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
            })

    token2 = json.loads(id3.text)['token']
    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token2,
            'channel_id': channel_id,
            'u_id': u_id1
        })
    assert resp1.status_code == 403


def test_no_perm_not_owner():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token1 = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token1,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    token2 = json.loads(id2.text)['token']
    u_id1 = json.loads(id2.text)['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'apple@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
            })
    u_id2 = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })
    
    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id2
        })

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token2,
            'channel_id': channel_id,
            'u_id': u_id2
        })
    assert resp1.status_code == 403

def test_no_perm_not_owner_invalid_u_id():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token1 = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token1,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    token2 = json.loads(id2.text)['token']
    u_id1 = json.loads(id2.text)['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'apple@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
            })
    u_id2 = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })
    
    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token2,
            'channel_id': channel_id,
            'u_id': -1
        })

    resp2 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token2,
            'channel_id': channel_id,
            'u_id': 123
        })
    assert resp1.status_code == 403
    assert resp2.status_code == 403

def test_no_perm_not_owner_u_id_not_member():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token1 = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token1,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    token2 = json.loads(id2.text)['token']
    u_id1 = json.loads(id2.text)['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'apple@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
            })
    u_id2 = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token2,
            'channel_id': channel_id,
            'u_id': u_id2
        })
    assert resp1.status_code == 403

def test_no_perm_not_owner_u_id_already_owner():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })

    token1 = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token1,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    token2 = json.loads(id2.text)['token']
    u_id1 = json.loads(id2.text)['auth_user_id']

    id3 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'apple@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'world'
            })
    u_id2 = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })
    
    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id2
        })

    requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id1
        })

    requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token1,
            'channel_id': channel_id,
            'u_id': u_id2
        })

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token2,
            'channel_id': channel_id,
            'u_id': u_id2
        })
        
    assert resp1.status_code == 403

def test_valid_addowner():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })
    token = json.loads(id1.text)['token']

    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })
    u_id = json.loads(id2.text)['auth_user_id']
    
    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })

    assert resp1.status_code == 200

def test_addowner_valid_global():
    requests.delete(config.url + "clear/v1")
    id1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'afirst',
            'name_last': 'alast'
        })
    token = json.loads(id1.text)['token']

    id2 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'elephant@gmail.com',
            'password': 'password',
            'name_first': 'kelly',
            'name_last': 'huang'
            })

    token2 = json.loads(id2.text)['token']
    ch1 = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token2,
            'name': '1531_CAMEl',
            'is_public': True
        })
    channel_id = json.loads(ch1.text)['channel_id']

    id3 = requests.post(config.url + "auth/register/v2", 
        json ={
            'email': 'hellokitty@gmail.com',
            'password': 'password',
            'name_first': 'hello',
            'name_last': 'kitty'
            })
    u_id = json.loads(id3.text)['auth_user_id']

    requests.post(config.url + 'channel/invite/v2', 
        json ={
            'token': token2,
            'channel_id': channel_id,
            'u_id': u_id
        })

    resp1 = requests.post(config.url + "channel/addowner/v1", 
        json = {
            'token': token,
            'channel_id': channel_id,
            'u_id': u_id
        })

    assert resp1.status_code == 200
