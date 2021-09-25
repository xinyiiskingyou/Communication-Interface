import pytest
from src.channel import channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v1, channels_list_v2
from src.auth import auth_register_v1

x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
x_channel = channels_create_v1(x_register['auth_user_id'], 'x', True)

sally_register = auth_register_v1('email1@gmail.com','comp1531', 'sally','zhou')
sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)

y_register = auth_register_v1('email2@gmail.com', 'password', 'y', 'lin')

def test_channel_invite_input_error():
    clear_v1()
    with pytest.raises(InputError):
        # channel_id does not refer to a valid channel
        channel_invite_v1(x_register['auth_user_id'], 1234, x_register['u_id'])
        channel_invite_v1(sally_register['auth_user_id'], 456, sally_register['u_id'])
        
        # u_id does not refer to a valid user
        channel_invite_v1(x_register['auth_user_id'], x_channel['channel_id'], 'hello')
        channel_invite_v1(sally_register['auth_user_id'], sally_channel['channel_id'], 'baka')


def test_channel_invite_access_error():

    # the authorised user is not a member of the channel
    clear_v1()
    with pytest.raises(AccessError):
        channel_invite_v1(x_register['auth_user_id'], x_channel['channel_id'], y_register['u_id'])
    
def test_valid_invite_public_member():
    
    # test if public channel member can invite new user
    channel_invite_v1(x_register['auth_user_id'], x_channel['channel_id'], y_register['u_id'])
    y_channel = channels_create_v1(y_register['auth_user_id'], 'y', False)

    assert(channels_list_v2(x_register['auth_user_id']) == {
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
				'channel_id': y_channel['channel_id'],
				'name': 'y'
			}
		],
	})

def test_valid_invite_private_member():

    # test if private channel member can invite new user
    z_register = auth_register_v1('email3@gmail.com', 'password', 'z', 'lin')
    channel_invite_v1(sally_register['auth_user_id'], sally_channel['channel_id'], z_register['u_id']) 
    z_channel = channels_create_v1(z_register['auth_user_id'], 'z', True)

    assert(channels_list_v2(sally_register['auth_user_id']) == {
		'channels': [
			{
				'channel_id': sally_channel['channel_id'],
				'name': 'sally'
			},
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
