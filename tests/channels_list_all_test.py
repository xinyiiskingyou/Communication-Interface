import pytest
from src.channels import channels_listall_v1, channels_create_v1, channels_list_v2
from src.data_store import data_store, initial_object
from src.auth import auth_register_v1
from src.other import clear_v1

def test_empty_channel(): 
    empty = auth_register_v1('email@gmail.com', 'password', 'hie', 'bye')
    assert(channels_listall_v1(empty) == {'channels':[]})

def test_channel_maker(): 
    a_register = auth_register_v1('ashemail@gmail.com', 'password', 'anna', 'wong')
    a_channel = channels_create_v1(a_register, 'anna', False)
    assert(channels_listall_v1(a_register) ==  
        {
            'channels' :[ 
                {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    'channel_id': a_channel,
                    'name': 'anna'
                },]
        })

def test_listall_channels():
    clear_v1()
    ash_register = auth_register_v1('ashley@gmail.com', 'ashpass', 'ashley', 'wong')
    a_register = auth_register_v1('ashemail@gmail.com', 'password', 'anna', 'wong')
    a_channel = channels_create_v1(a_register, 'anna', False)
    ash_channel = channels_create_v1(ash_register, 'ashley', False)
    ashv1_channel = channels_create_v1(ash_register, 'ash', True)
    assert (channels_listall_v1(ash_register) == 
        {
            'channels' :[
                {
                    'channel_id': a_channel,
                    'name': 'anna' 
                }, 
                {
                    'channel_id' : ash_channel,
                    'name' : 'ashley'
                },
                {
                    'channel_id' : ashv1_channel,
                    'name' : 'ash' 
                }

            ],
        })
    assert ((channels_listall_v1(ash_register))== (channels_list_v2(ash_register)))