from src.channels import channels_list_v1, channels_create_v1
from src.auth import auth_register_v1

# using auth_register to get the auth_user_id 
id = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
id1 = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
id2 = auth_register_v1('email3@gmail.com', 'comp1521', 'chris','sun')
no_channel = auth_register_v1('email1@gmail.com', 'Password1', 'anna','duong')

# since channels_create function returns channel_id
# call channels_create function to get the channel_id
new_channel = channels_create_v1(id['auth_user_id'], 'x', True)
chris_channel = channels_create_v1(id2['auth_user_id'],'chris', True)
sally_channel = channels_create_v1(id1['auth_user_id'], 'sally', False)

# test if a user only has id but dosen't have channel
# it should return empty
def test_no_channels():
    assert(channels_create_v1(no_channel['auth_user_id']) == {
        'channels': []
    })

# test if it can successfully return if a person has channel and id
def test_channels_list():
    assert(channels_list_v1(id['auth_user_id']) ==
    {
        'channels': [
        	{
        		'channel_id': new_channel['channel_id'],
        		'name': 'x_channel'
        	}
        ],
    })

# test if there are 2 ppl join the channels
def test_two_users():
    assert(channels_create_v1(id1['auth_user_id']) == {
        'channels': [
            {
        		'channel_id': sally_channel['channel_id'],
        		'name': 'sally_channel'
        	},
        	{
        		'channel_id': new_channel['channel_id'],
        		'name': 'x_channel'
        	}
        ],
    })

def test_more_users():
    assert(channels_create_v1(id2['auth_user_id']) == {
        'channels': [
            {
        		'channel_id': chris_channel['channel_id'],
        		'name': 'chris_channel'
        	},
            {
        		'channel_id': sally_channel['channel_id'],
        		'name': 'sally_channel'
        	},
        	{
        		'channel_id': new_channel['channel_id'],
        		'name': 'x_channel'
        	}
        ],
    })