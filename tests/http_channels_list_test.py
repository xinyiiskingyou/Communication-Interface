import pytest
import requests
import json
from src import config
from src.other import clear_v1 

##########################################
######### channels_list tests ##########
##########################################

# test when an user does not create a channel
def test_no_channel():
    requests.delete(config.url + "clear/v1", json={})

    resp = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'sally123@gmail.com', 
        'password': 'password1234', 
        'name_first': 'sally', 
        'name_last': 'wong'
    })

    response_data = resp.json()
    token = response_data['token']
    list = requests.get(config.url + 'channels/list/v2', params ={
        'token': token
    })
    assert json.loads(list.text) == {'channels': []}
    assert list.status_code == 200

# test one user creates a channel and can be appended in the list
def test_channel_list():
    requests.delete(config.url + "clear/v1", json={})

    resp = requests.post(config.url + 'auth/register/v2', 
        json ={
            'email': 'anna345@gmail.com', 
            'password': 'password123', 
            'name_first': 'anna', 
            'name_last': 'wong'
        })

    response_data = resp.json()
    token = response_data['token']

    channel = requests.post(config.url + "channels/create/v2", 
        json = {
            'token': token,
            'name': '1531_CAMEL',
            'is_public': False
        })

    channel_id1 = json.loads(channel.text)['channel_id']
    assert channel_id1 != None
    
    list1 = requests.get(config.url + 'channels/list/v2', params ={
        'token': token
    })
    assert (json.loads(list1.text) == 
        {
        'channels':[
            {
                'channel_id': channel_id1,
                'name': '1531_CAMEL',
            }
        ],
    })
    assert list1.status_code == 200

