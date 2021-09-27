import pytest
from src.channels import channels_list_v2, channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.data_store import data_store
from src.error import InputError

# test if a user is authorised but dosen't have channel
# it should return empty
def test_no_channels():
	clear_v1()
	no_channel = auth_register_v1('email1@gmail.com', 'Password1', 'anna','duong')
	assert(channels_list_v2(no_channel['auth_user_id']) == {'channels':[]})

# test if more and more authorised users can be appended in the list 
def test_channels_list():
	
	clear_v1()
	x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
	x_channel = channels_create_v1(x_register['auth_user_id'], 'x', True)
	assert(channels_list_v2(x_register['auth_user_id']) ==
		{
		'channels':[
		{
			'channel_id': x_channel['channel_id'],
			'name': 'x'
        },
		]
		})

	# test if there are 2 authorised users join the channels
	# and including the private channels
	sally_register = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
	sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)
	assert(channels_list_v2(sally_register['auth_user_id']) == {
		'channels': [
			{
				'channel_id': x_channel['channel_id'],
				'name': 'x'
			},
			{
				'channel_id': sally_channel['channel_id'],
				'name': 'sally'
			}
		],
	})

	emma_register = auth_register_v1('email3@gmail.com', 'comp1521', 'emma','sun')
	emma_channel = channels_create_v1(emma_register ['auth_user_id'],'emma', True)
	assert(channels_list_v2(emma_register['auth_user_id']) == {
		'channels': [
			{
				'channel_id': x_channel['channel_id'],
				'name': 'x'
			},

			{
				'channel_id': sally_channel['channel_id'],
				'name': 'sally'
			},

			{
				'channel_id': emma_channel['channel_id'],
				'name': 'emma'
			}
		],
	})

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
    with pytest.raises(InputError):
        channels_create_v1('', '1531_CAMEL', 1)
    clear_v1()
    with pytest.raises(InputError):
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

