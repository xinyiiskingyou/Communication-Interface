import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_messages_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1

# Public: channel_id does not refer to a valid channel
def test_channel_invalid_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	auth_user_id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
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
	with pytest.raises(InputError):
		channel_details_v1(auth_user_id2['auth_user_id'], 0)
		channel_details_v1(auth_user_id2['auth_user_id'], -1)
		channel_details_v1(auth_user_id2['auth_user_id'], -116)

		channel_invite_v1(auth_user_id2['auth_user_id'], -1, auth_user_id1)
		channel_invite_v1(auth_user_id2['auth_user_id'], -116, auth_user_id1)

		channel_join_v1(auth_user_id1['auth_user_id'], -1)
		channel_join_v1(auth_user_id1['auth_user_id'], -116)

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

##########################################
########### channel_invite tests #########
##########################################

# Input error when the user has invalid u_id
def test_invite_invalid_u_id():
	clear_v1()
	auth_user_id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
	channel_id = channels_create_v1(auth_user_id1['auth_user_id'], 'anna', True)
	with pytest.raises(InputError):
		channel_invite_v1(auth_user_id1['auth_user_id'], channel_id['channel_id'], 115)
		channel_invite_v1(auth_user_id1['auth_user_id'], channel_id['channel_id'], -116)

# Test if public channel member can invite new user
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

# Test if private channel member can invite new user
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

##########################################
########### channel_join tests ###########
##########################################

# Input error when the authorised user is already a member of the channel
def test_join_already_in(): 
    clear_v1()
    a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
    a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', True)
    with pytest.raises(InputError): 
        channel_join_v1(a_register['auth_user_id'], a_channel['channel_id'])

# AccessError when channel_id refers to a channel that is private 
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

# Test channel_join function
def test_valid_channel_join (): 
	clear_v1()
	a_register = auth_register_v1('email@gmail.com', 'password', 'lily','wong')
	a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', True)
	j_register = auth_register_v1('ashemail@gmail.com', 'password', 'jilly','wong')
	channel_join_v1(j_register['auth_user_id'], a_channel['channel_id'])
	assert channel_details_v1(j_register['auth_user_id'], a_channel['channel_id']) == (
	channel_details_v1(a_register['auth_user_id'], a_channel['channel_id']))


##########################################
######### channel_messages tests #########
##########################################

########## Implementation Tests (To be completed when adding messages is added) ##########

# Start at most recent message (index = 0) and number of messages > 50


# Start at most recent message (index = 0) and number of messages < 50


# Start at most recent message (index = 0) and number of messages = 50


# Start at neither most or least recent and number of messages > 50


# Start at neither most or least recent and number of messages < 50


# No messages currently in channel
def test_no_messages():
    clear_v1()
    r_user_id = auth_register_v1('rebecca@gmail.com', 'rebeccapass', 'rebecca', 'hsu')
    r_channel_id = channels_create_v1(r_user_id['auth_user_id'], 'rebecca_channel', False)
    assert (channel_messages_v1(r_user_id['auth_user_id'], r_channel_id['channel_id'], 0) == 
        {
            'messages' :[],
            'start': 0, 
            'end': -1
        }
    )

########## Input Error Tests ##########
# channel_id does not refer to a valid channel
def test_invalid_channel_id():
    clear_v1()
    r_user_id = auth_register_v1('rebecca@gmail.com', 'rebeccapass', 'rebecca', 'hsu')
    channels_create_v1(r_user_id['auth_user_id'], 'rebecca_channel', False)
    with pytest.raises(InputError):
        channel_messages_v1(r_user_id['auth_user_id'], -1, 0)


# Start is greater than the total number of messages in the channel
def test_start_gt_total_messages():
    clear_v1()
    r_user_id = auth_register_v1('rebecca@gmail.com', 'rebeccapass', 'rebecca', 'hsu')
    r_channel_id = channels_create_v1(r_user_id['auth_user_id'], 'rebecca_channel', False)
    with pytest.raises(InputError):
        channel_messages_v1(r_user_id['auth_user_id'], r_channel_id['channel_id'], 10)


########## Access Error Tests ##########
# channel_id is valid and the authorised user is not a member of the channel 
def test_user_not_authorised_to_channel():
    clear_v1()
    r_user_id = auth_register_v1('rebecca@gmail.com', 'rebeccapass', 'rebecca', 'hsu')
    r_channel_id = channels_create_v1(r_user_id['auth_user_id'], 'rebecca_channel', False)
    a_user_id = auth_register_v1('ashley@gmail.com', 'ashleypass', 'ashley', 'wong')
    with pytest.raises(AccessError):
        channel_messages_v1(a_user_id['auth_user_id'], r_channel_id['channel_id'], 0)
