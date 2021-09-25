import pytest
from src.channels import channels_listall_v1, channels_create_v1
from src.data_store import data_store, initial_object
from src.auth import auth_register_v1
def test_empty_channel(): 
    empty = auth_register_v1('email@gmail.com', 'password', 'hie', 'bye')
    assert(channels_listall_v1(empty['auth_user_id']) == {'channels':[]})

def test_channel_maker(): 
    a_register = auth_register_v1('ashemail@gmail.com', 'password', 'anna', 'wong')
    a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', False)
    assert(channels_listall_v1(a_register['auth_user_id']) ==  
            'channels' :[ 
                {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    'channel_id': a_channel['channel_id'],
                    'name': 'anna'
                },]
        })

def test_listall_channels(): 
    ash_register = auth_register_v1('ashley@gmail.com', 'ashpass', 'ashley', 'wong')
    ash_channel = channels_create_v1(ash_register['auth_user_id'], 'ashley', False)
    ashv1_channel = channels_create_v1(ash_register['auth_user_id'], 'ash', True)
    assert (channels_listall_v1(ash_register['auth_user_id']) == 
        {
            'channels' :[ 
                {
                    'channel_id' : ash_channel['channel_id'],
                    'name' : 'ashley'
                },
                {
                    'channel_id' : ashv1_channel['channel_id'],
                    'name' : 'ash' 
                }
            ],
        })