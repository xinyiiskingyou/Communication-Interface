import pytest 
from src.other import clear_v1
import requests
from src import config
import json 


BASE_URL = 'http://127.0.0.1:8080'

def test_listall_http(): 
    requests.delete(config.url + "clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'abc@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        })
    token1 = json.loads(user1.text)['token']
    response_data = user1.json()
    channel1 = requests.post(config.url + "channels/create/v2", 
        json = {
        'token': token1,
        'name': 'channel1',
        'is_public': True
    })
    channel_id1 = json.loads(channel1.text)['channel_id']
    assert channel_id1 != None
    listall1 = requests.get(config.url + "channels/list/all/v1", 
        params = { 
            'token': token1
        })
    assert (json.loads(listall1.text) == 
        {
        'channels':[
            {
                'channel_id': channel_id1,
                'name': 'channel1',
            }
        ],
    })

    assert response1.status_code == 200

