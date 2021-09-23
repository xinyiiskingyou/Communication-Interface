import pytest
from src.channels import channels_list_v1, channels_create_v1
from src.auth import auth_register_v1

# test if a user is authorised but dosen't have channel
# it should return empty
def test_no_channels():
	no_channel = auth_register_v1('email1@gmail.com', 'Password1', 'anna','duong')
	assert(channels_list_v1(no_channel['auth_user_id']) == {'channels':[]})

# test if more and more authorised users can be appended in the list 
def test_channels_list():

	x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
	x_channel = channels_create_v1(x_register['auth_user_id'], 'x', True)
	assert(channels_list_v1(x_register['auth_user_id']) ==
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
	assert(channels_list_v1(sally_register['auth_user_id']) == {
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
	assert(channels_list_v1(emma_register['auth_user_id']) == {
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

