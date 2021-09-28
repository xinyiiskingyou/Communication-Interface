import pytest
from src.channels import channels_list_v2, channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError

# InputError when length of name is less than 1 or more than 20 characters
def test_create_invalid_name():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
        channels_create_v1(1, '', 1)
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
        channels_create_v1(1, ' ', 1)
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
        channels_create_v1(1, '                      ', 1)
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
        channels_create_v1(1, 'abcdefghijklmlaqwertq', 1)

def test_create_valid_public():
    clear_v1()
    auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channels_create_v1(1, '1531_CAMEL', 1)

def test_create_valid_private():
    clear_v1()
    auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channels_create_v1(1, 'channel', 0)

def test_create_invalid_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1('', '1531_CAMEL', 1)
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1('not_a_id', '1531_CAMEL', 1)

def test_create_invalid_public():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
        channels_create_v1(1, '1531_CAMEL', -1)
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
        channels_create_v1(1, '1531_CAMEL', 100)

def test_create_invalid_channel_id():
    clear_v1()
    auth_id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channel_id = channels_create_v1(auth_id, '1531_CAMEL', 0)
    assert channel_id != -1

'''
The following functions test both channels_list and channel_list_all function
'''
# test if an authorised user that dosen't have channel
# it should return empty
def test_no_channels():

	clear_v1()
	no_channel = auth_register_v1('email1@gmail.com', 'Password1', 'anna','duong')
	assert(channels_list_v2(no_channel) == {'channels':[]})
	assert(channels_listall_v1(no_channel) == {'channels':[]})
	assert(channels_list_v2(no_channel)) == channels_listall_v1(no_channel)

# test if more and more authorised users can be appended in the list 
def test_channels_list():
	
	clear_v1()
    # test if public channel can be appened in the list
	x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
	x_channel = channels_create_v1(x_register, 'x', True)
	assert(channels_list_v2(x_register) ==
		{
		'channels':[
		{
			'channel_id': x_channel,
			'name': 'x'
        },
		]
	})

	assert(channels_listall_v1(x_register) ==  
        {
            'channels' :[ 
                {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                    'channel_id': x_channel,
                    'name': 'x'
                },]
    })

	assert(channels_list_v2(x_register)) == channels_listall_v1(x_register)

    # test if private channels can be appened in the list
	sally_register = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
	sally_channel = channels_create_v1(sally_register, 'sally', False)
	assert(channels_list_v2(sally_register) == {
		'channels': [
			{
				'channel_id': x_channel,
				'name': 'x'
			},
			{
				'channel_id': sally_channel,
				'name': 'sally'
			}
		],
	})

	emma_register = auth_register_v1('email3@gmail.com', 'comp1521', 'emma','sun')
	emma_channel = channels_create_v1(emma_register,'emma', True)
	assert(channels_list_v2(emma_register) == {
		'channels': [
			{
				'channel_id': x_channel,
				'name': 'x'
			},

			{
				'channel_id': sally_channel,
				'name': 'sally'
			},

			{
				'channel_id': emma_channel,
				'name': 'emma'
			}
		],
	})

# Test channels_list_all function
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


def test_empty_channel():
    clear_v1()
    empty = auth_register_v1('email@gmail.com', 'password', 'hie', 'bye')
    assert(channels_listall_v1(empty) == {'channels':[]})

def test_channel_maker():
    clear_v1()
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
