import pytest
import requests
import json
from src import config 
from src.other import clear_v1

##########################################
######### channels_list tests ##########
##########################################
def test_no_channel():
    
    resp = requests.get(config.url + 'auth/register/v2', json ={
        'email': 'cat@gmail.com', 
        'password': 'password1234', 
        'name_first': 'sally', 
        'name_last': 'wong'
    })
    response_data = resp.json

    list = requests.get(config.url + 'channels/list/v2', json = {
        'token': response_data['token']
    })

    assert json.loads(list.text) == {[]}
    assert list.status_code == 200


def test_channel_list():

    resp = requests.get(config.url + 'auth/register/v2', json ={
        'email': 'abc@gmail.com', 
        'password': 'password123', 
        'name_first': 'anna', 
        'name_last': 'wong'
    })
    response_data = resp.json
    
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': response_data['token'],
        'name': 'new_channel',
        'is_pulic': True
    })
    channel_data = channel.json
    assert channel_data['channel_id'] != None

    list = requests.get(config.url + 'channels/list/v2', json = {
        'token': response_data['token']
    })

    assert json.loads(list.text) == {
        'channel_id': channel_data['channel_id'],
        'name': 'new_channel'
    }
    assert list.status_code == 200
