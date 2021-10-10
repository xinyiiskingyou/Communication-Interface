import pytest
import requests
import json
from src import config 
from src.other import clear_v1

##########################################
######### channels_list tests ##########
##########################################

def test_no_channel():
    
    resp = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'sally123@gmail.com', 
        'password': 'password1234', 
        'name_first': 'sally', 
        'name_last': 'wong'
    })
    response_data = resp.json()
    token = response_data['token']
    list = requests.get(config.url + 'channels/list/v2', json = {
        'token': token
    })
    assert list.status_code == 200

def test_channel_list():
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', json ={
        'email': 'anna345@gmail.com', 
        'password': 'password123', 
        'name_first': 'anna', 
        'name_last': 'wong'
    })
    response_data = resp.json()
    token = response_data['token']

    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': token,
        'name': 'new_channel',
        'is_pulic': True
    })

    channel_data = channel.json()
    list = requests.get(config.url + 'channels/listall/v2', json = {
        'token': token
    })

    assert json.loads(list.text) == {
        'channel_id': channel_data['channel_id'],
        'name': 'new_channel'
    }
    assert list.status_code == 200
