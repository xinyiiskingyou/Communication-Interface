import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1

# Public: channel_id does not refer to a valid channel
def test_channel_invalid_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2['auth_user_id'], 'anna', True)
	with pytest.raises(InputError):
		channel_details_v1(auth_user_id1['auth_user_id'], 0)
		channel_details_v1(auth_user_id1['auth_user_id'], -1)
		channel_details_v1(auth_user_id1['auth_user_id'], -116)
		
		channel_invite_v1(auth_user_id1['auth_user_id'], -1, auth_user_id2)
		channel_invite_v1(auth_user_id1['auth_user_id'], -116, auth_user_id2)

		channel_join_v1(auth_user_id1['auth_user_id'], 3456)

# Private: channel_id does not refer to a valid channel
def test_channel_invalid_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2['auth_user_id'], 'anna', False)
	with pytest.raises(InputError):
		channel_details_v1(auth_user_id2['auth_user_id'], 0)
		channel_details_v1(auth_user_id2['auth_user_id'], -1)
		channel_details_v1(auth_user_id2['auth_user_id'], -116)

		channel_invite_v1(auth_user_id2['auth_user_id'], -1, auth_user_id1)
		channel_invite_v1(auth_user_id2['auth_user_id'], -116, auth_user_id1)

		channel_join_v1(auth_user_id1['auth_user_id'], -1)

# Public: Authorised user is not a memner of the channel
def test_channel_not_member():
	clear_v1()
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id3 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2['auth_user_id'], 'anna', True)

	with pytest.raises(AccessError):
		channel_details_v1(auth_user_id2, auth_user_id3['auth_user_id'])
		channel_invite_v1(auth_user_id2['auth_user_id'], channel_id['channel_id'], auth_user_id3['auth_user_id'])

# Private: Authorised user is not a memner of the channel
def test_channel_not_member():
	clear_v1()
	auth_user_id2 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id3 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id2['auth_user_id'], 'anna', False)
	with pytest.raises(AccessError):
		channel_details_v1(auth_user_id3['auth_user_id'], 1)
		channel_invite_v1(auth_user_id2['auth_user_id'], channel_id['channel_id'], auth_user_id3['auth_user_id'])

# channel_invite function: Input error when the user has invalid u_id
def test_invite_invalid_u_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id1['auth_user_id'], 'anna', True)
	with pytest.raises(InputError):
		channel_invite_v1(auth_user_id1['auth_user_id'], channel_id['channel_id'], -1)
		channel_invite_v1(auth_user_id1['auth_user_id'], channel_id['channel_id'], -116)

# channel_join function: Input error when the authorised user is already a member of the channel
def test_join_already_in(): 
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', True)
    with pytest.raises(InputError): 
        channel_join_v1(a_register['auth_user_id'], a_channel['channel_id'])

# channel_join function: AccessError when channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
def test_join_access_error (): 
	clear_v1()
	a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
	a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', False)
	j_register = auth_register_v1('ashemail@gmail.com', 'password', 'jilly','wong')
	with pytest.raises(AccessError): 
		channel_join_v1(j_register['auth_user_id'], a_channel['channel_id'])

	clear_v1()
	a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
	a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', True)
	with pytest.raises(AccessError):
		channel_join_v1(123, a_channel['channel_id'])

# channel invite function: Test if public channel member can invite new user
def test_valid_invite_member():
	clear_v1()
	# create a public channel
	x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
	x_channel = channels_create_v1(x_register['auth_user_id'], 'x', True)
	# create an auth_user but currently did not join the channel
	y_register = auth_register_v1('email2@gmail.com', 'password', 'y', 'lin')
	y_channel = channels_create_v1(y_register['auth_user_id'], 'y', False)

	channel_invite_v1(x_register['auth_user_id'], x_channel['channel_id'], y_register['auth_user_id'])
	assert(channels_listall_v1(x_register['auth_user_id']) == {
		'channels': [
			{
				'channel_id': x_channel['channel_id'],
				'name': 'x'
			},
			{
				'channel_id': y_channel['channel_id'],
				'name': 'y'
			}
		],
	})

# channel invite function: test if private channel member can invite new user
def test_valid_invite_member_private():
	clear_v1()
	# create a private channel
	sally_register = auth_register_v1('email1@gmail.com', 'comp1531', 'sally', 'zhou')
	sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)

	z_register = auth_register_v1('email3@gmail.com', 'password', 'z', 'lin')
	channel_invite_v1(sally_register['auth_user_id'], sally_channel['channel_id'], z_register['auth_user_id']) 
	z_channel = channels_create_v1(z_register['auth_user_id'], 'z', True)

	assert(channels_listall_v1(sally_register['auth_user_id']) == {
		'channels': [
			{
				'channel_id': sally_channel['channel_id'],
				'name': 'sally'
			},
			{
				'channel_id': z_channel['channel_id'],
				'name': 'z'
			}
		],
	})

# Test channel_join function
def test_valid_channel_join (): 
	clear_v1()
	a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
	a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', True)
	j_register = auth_register_v1('ashemail@gmail.com', 'password', 'jilly','wong')
	channel_join_v1(j_register['auth_user_id'], a_channel['channel_id'])
	assert channel_details_v1(j_register['auth_user_id'], a_channel['channel_id']) == (
	channel_details_v1(a_register['auth_user_id'], a_channel['channel_id']))