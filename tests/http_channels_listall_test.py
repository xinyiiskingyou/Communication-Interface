import pytest 
from src.other import clear_v1
import requests
from src import config
import json 


BASE_URL = 'http://127.0.0.1:8080'

def test_listall_http(): 
    requests.delete(config.url + "clear/v1")
    response1 = requests.get(config.url + "channels/list/all/v2", 
        json = { 
            'channels':[
                {
                    'channel_id': id2_channel['channel_id'],
                    'name': 'anna'
                },
            ]
        }) 
    assert response1.status_code == 400