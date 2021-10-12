import pytest
import requests
import json
from src import config

#valid 
def test_http_join (): 
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

    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': True
    })
    channel_id1 = json.loads(channel1.text)['channel_id']
    assert channel_id1 == json.loads(channel1.text)['channel_id']

    respo1 = requests.post(config.url + "channel/join/v2",
        json = { 
        'token': token2, 
        'channel_id': json.loads(channel1.text)['channel_id'],
        })
    assert respo1.status_code == 200

#Invalid channel_id 
def test_invalid_join_channel_id():
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

    invite = requests.post(config.url + 'channel/invite/v2', json ={
        'token': token,
        'channel_id': -16,
    })
    assert invite.status_code == 400

