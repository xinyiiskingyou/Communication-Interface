import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1

# Public: Invalid channel_id 
def test_c_details_invalid_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2, 'anna', True)
	with pytest.raises(InputError):
		channel_details_v1(auth_user_id1, 0)
		channel_details_v1(auth_user_id1, -1)
		channel_details_v1(auth_user_id1, -116)
		
		channel_invite_v1(auth_user_id1, -1, auth_user_id2)
		channel_invite_v1(auth_user_id1, -116, auth_user_id2)

# Private: Invalid channel_id 
def test_c_details_invalid_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2, 'anna', True)
	with pytest.raises(InputError):
		channel_details_v1(auth_user_id2, 0)
		channel_details_v1(auth_user_id2, -1)
		channel_details_v1(auth_user_id2, -116)

		channel_invite_v1(auth_user_id2, -1, auth_user_id1)
		channel_invite_v1(auth_user_id2, -116, auth_user_id1)

# Public: Authorised user is not a memner of the channel
def test_c_details_not_member():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id3 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2, 'anna', True)

	with pytest.raises(AccessError):
		channel_details_v1(auth_user_id1, 1)
		channel_invite_v1(auth_user_id2, channel_id, auth_user_id3)


# Private: Authorised user is not a memner of the channel
def test_c_details_not_member():
	clear_v1()
	auth_user_id2 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id3 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2, 'anna', False)
	with pytest.raises(AccessError):
		channel_details_v1(auth_user_id3, 1)
		channel_invite_v1(auth_user_id2, channel_id, auth_user_id3)

# Test Invalid u_id
def test_invalid_u_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id1, 'anna', True)
	with pytest.raises(InputError):
		channel_invite_v1(auth_user_id1, channel_id, -1)
		channel_invite_v1(auth_user_id1, channel_id, -116)

def test_valid_invite_member():
	
	clear_v1()
	# create a public channel
	x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
	x_channel = channels_create_v1(x_register, 'x', True)
	# create an auth_user but currently did not join the channel
	y_register = auth_register_v1('email2@gmail.com', 'password', 'y', 'lin')
	y_channel = channels_create_v1(y_register, 'y', False)

	# test if public channel member can invite new user
	channel_invite_v1(x_register, x_channel, y_register)
	assert(channels_listall_v1(x_register) == {
		'channels': [
			{
				'channel_id': x_channel,
				'name': 'x'
			},
			{
				'channel_id': y_channel,
				'name': 'y'
			}
		],
	})

# test if private channel member can invite new user
def test_valid_invite_member_private():
	clear_v1()
	# create a private channel
	sally_register = auth_register_v1('email1@gmail.com', 'comp1531', 'sally', 'zhou')
	sally_channel = channels_create_v1(sally_register, 'sally', False)

	z_register = auth_register_v1('email3@gmail.com', 'password', 'z', 'lin')
	channel_invite_v1(sally_register, sally_channel, z_register) 
	z_channel = channels_create_v1(z_register, 'z', True)

	assert(channels_listall_v1(sally_register) == {
		'channels': [
			{
				'channel_id': sally_channel,
				'name': 'sally'
			},
			{
				'channel_id': z_channel,
				'name': 'z'
			}
		],
	})


def test_input_invalid_channel():
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    with pytest.raises(InputError):
        channel_join_v1(a_register, 3456)

def test_already_in(): 
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    a_channel = channels_create_v1(a_register, 'anna', True)
    with pytest.raises(InputError): 
        channel_join_v1(a_register, a_channel)
    
def test_AccessError (): 
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    a_channel = channels_create_v1(a_register, 'anna', False)
    j_register = auth_register_v1('ashemail@gmail.com', 'password', 'jilly','wong')
    with pytest.raises(AccessError): 
            channel_join_v1(j_register, a_channel)


def test_authuser_AccessError (): 
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    a_channel = channels_create_v1(a_register, 'anna', True)
    with pytest.raises(AccessError):
        channel_join_v1(123, a_channel)

def test_join (): 
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    a_channel = channels_create_v1(a_register, 'anna', True)
    j_register = auth_register_v1('ashemail@gmail.com', 'password', 'jilly','wong')
    channel_join_v1(j_register, a_channel)
    assert channel_details_v1(j_register, a_channel) == channel_details_v1(a_register, a_channel)