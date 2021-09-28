import pytest
from src.channel import channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v1, channels_list_v2, channels_listall_v1
from src.auth import auth_register_v1

# create a public channel
x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
x_channel = channels_create_v1(x_register, 'x', True)
# create a private channel
sally_register = auth_register_v1('email1@gmail.com', 'comp1531', 'sally', 'zhou')
sally_channel = channels_create_v1(sally_register, 'sally', False)
# create an auth_user but currently did not join the channel
y_register = auth_register_v1('email2@gmail.com', 'password', 'y', 'lin')

# input error
def test_channel_invite_input_error():

    with pytest.raises(InputError):
        # channel_id does not refer to a valid channel
        channel_invite_v1(x_register, 1234, y_register)
        channel_invite_v1(sally_register, 456, y_register)
        
        # u_id does not refer to a valid user
        channel_invite_v1(x_register, x_channel, '0')
        channel_invite_v1(sally_register, sally_channel, '-1')

# Access error when channel_id is valid and the authorised user is not a member of the channel
def test_channel_invite_access_error():
    with pytest.raises(AccessError):
        channel_invite_v1(x_register, sally_channel, y_register)

y_channel = channels_create_v1(y_register, 'y', False)
def test_valid_invite_public_member():

	# test if public channel member can invite new user
	channel_invite_v1(x_register, x_channel, y_register)
	assert(channels_listall_v1(x_register) == {
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
				'channel_id': y_channel,
				'name': 'y'
			}
		],
	})

	# test if private channel member can invite new user
	z_register = auth_register_v1('email3@gmail.com', 'password', 'z', 'lin')
	channel_invite_v1(sally_register, sally_channel, z_register) 
	z_channel = channels_create_v1(z_register, 'z', True)

	assert(channels_listall_v1(sally_register) == {
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
				'channel_id': y_channel,
				'name': 'y'
			},
			{
				'channel_id': z_channel,
				'name': 'z'
			}
			
		],
	})
