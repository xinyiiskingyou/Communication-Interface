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


