import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_messages_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1

##########################################
########## channel_invite tests ##########
##########################################

# Invalid auth_user_id
def test_invite_auth_user_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id2['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError):

        # Public
        channel_invite_v1(-16, channel_id2['channel_id'], id1['auth_user_id'])
        channel_invite_v1(0, channel_id2['channel_id'], id3['auth_user_id'])
        channel_invite_v1(256, channel_id2['channel_id'], id4['auth_user_id'])
        channel_invite_v1('', channel_id2['channel_id'], id1['auth_user_id'])
        channel_invite_v1('not_an_id', channel_id2['channel_id'], id4['auth_user_id'])

        #Private
        channel_invite_v1(-16, channel_id4['channel_id'], id2['auth_user_id'])
        channel_invite_v1(0, channel_id4['channel_id'], id3['auth_user_id'])
        channel_invite_v1(256, channel_id4['channel_id'], id1['auth_user_id'])
        channel_invite_v1('', channel_id4['channel_id'], id1['auth_user_id'])
        channel_invite_v1('not_an_id', channel_id4['channel_id'], id3['auth_user_id'])

# Invalid u_id
def test_invite_u_id():
    clear_v1()
    id2 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(InputError):

        # Public 
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], -16)
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], 0)
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], 256)
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], '')
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], 'not_an_id')

        # Private
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], -16)
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], 0)
        channel_invite_v1(id4['auth_user_id'], channel_id24['channel_id'], 256)
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], '')
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], 'not_an_id')



# Invalid channel_id - id1 invites id2
def test_invite_channel_id_1():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], -16, id2['auth_user_id'])
        channel_invite_v1(id1['auth_user_id'], 0, id2['auth_user_id'])
        channel_invite_v1(id1['auth_user_id'], 256, id2['auth_user_id'])
        channel_invite_v1(id1['auth_user_id'], '', id2['auth_user_id'])
        channel_invite_v1(id1['auth_user_id'], 'not_an_id', id2['auth_user_id'])

# Invalid channel_id - id2 invites id1
def test_invite_channel_id_2():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], -16, id1['auth_user_id'])
        channel_invite_v1(id2['auth_user_id'], 0, id1['auth_user_id'])
        channel_invite_v1(id2['auth_user_id'], 256, id1['auth_user_id'])
        channel_invite_v1(id2['auth_user_id'], '', id1['auth_user_id'])
        channel_invite_v1(id2['auth_user_id'], 'not_an_id', id1['auth_user_id'])

# Public: u_id refers to a user who is already a member of the channel
def test_invite_already_member_pub():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    
    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    channel_join_v1(id3['auth_user_id'], channel_id2['channel_id'])

    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], id1['auth_user_id'])
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], id3['auth_user_id'])
        # WHen someone tries to invite owner
        channel_invite_v1(id1['auth_user_id'], channel_id2['channel_id'], id2['auth_user_id'])

# Private: u_id refers to a user who is already a member of the channel
def test_invite_already_member_priv():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id1['auth_user_id'])
    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])

    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id1['auth_user_id'])
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])

        # WHen someone tries to invite owner
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], id4['auth_user_id'])

# Authorised user is not a memnber of the channel
def test_invite_not_member1():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id2['auth_user_id'], 'shelly', False)
    
    with pytest.raises(AccessError):

        # Public
        channel_invite_v1(id1['auth_user_id'], channel_id2['channel_id'], id3['auth_user_id'])
        channel_invite_v1(id1['auth_user_id'], channel_id2['channel_id'], id2['auth_user_id'])

        # Private
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], id1['auth_user_id'])
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], id4['auth_user_id'])

# Public: Test channel_invite function
def test_valid_channel_invite_pub(): 
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], id1['auth_user_id'])
    details1 = channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details2 = channel_details_v1(id2['auth_user_id'], channel_id2['channel_id'])
    assert details1 == details2

# Private: Test channel_invite function
def test_valid_channel_invite_priv(): 
    clear_v1()
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id3['auth_user_id'])
    details3 = channel_details_v1(id3['auth_user_id'], channel_id4['channel_id'])
    details4 = channel_details_v1(id4['auth_user_id'], channel_id4['channel_id'])
    assert details3 == details4

##########################################
######### channel_details tests ##########
##########################################

# Invalid auth_user_id
def test_details_auth_user_id():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id2['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError):

        #Public
        channel_details_v1(-1, channel_id2['channel_id'])
        channel_details_v1(0, channel_id2['channel_id'])
        channel_details_v1(256, channel_id2['channel_id'])
        channel_details_v1('', channel_id2['channel_id'])
        channel_details_v1('not_an_id', channel_id2['channel_id'])
        

        #Private
        channel_details_v1(-1, channel_id4['channel_id'])
        channel_details_v1(0, channel_id4['channel_id'])
        channel_details_v1(256, channel_id4['channel_id'])
        channel_details_v1('', channel_id4['channel_id'])
        channel_details_v1('not_an_id', channel_id4['channel_id'])

# Invalid channel_id
def test_details_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')

    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], -1)
        channel_details_v1(id1['auth_user_id'], 0)
        channel_details_v1(id1['auth_user_id'], 256)
        channel_details_v1(id1['auth_user_id'], '')
        channel_details_v1(id1['auth_user_id'], 'not_an_id')

# Authorised user is not a member of the channel
def test_details_not_member():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id2['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError):

        # Public
        channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
        channel_details_v1(id4['auth_user_id'], channel_id2['channel_id'])

        # Private
        channel_details_v1(id2['auth_user_id'], channel_id4['channel_id'])
        channel_details_v1(id3['auth_user_id'], channel_id4['channel_id'])

##########################################
######### channel_messages tests #########
##########################################

########## Implementation Tests (To be completed when adding messages is added) ##########

# Start at most recent message (index = 0) and number of messages > 50


# Start at most recent message (index = 0) and number of messages < 50


# Start at most recent message (index = 0) and number of messages = 50


# Start at neither most or least recent and number of messages > 50


# Start at neither most or least recent and number of messages < 50


# Inavlid auth_user_id
def test_messages_auth_user_id():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id2['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError):

        # Public
        channel_messages_v1(-16, channel_id2['channel_id'], 0)
        channel_messages_v1(0, channel_id2['channel_id'], 0)
        channel_messages_v1(256, channel_id2['channel_id'], 0)
        channel_messages_v1('', channel_id2['channel_id'], 0)
        channel_messages_v1('not_an_id', channel_id2['channel_id'], 0)

        # Private
        channel_messages_v1(-16, channel_id4['channel_id'], 0)
        channel_messages_v1(0, channel_id4['channel_id'], 0)
        channel_messages_v1(256, channel_id4['channel_id'], 0)
        channel_messages_v1('', channel_id4['channel_id'], 0)
        channel_messages_v1('not_an_id', channel_id4['channel_id'], 0)

# channel_id does not refer to a valid channel
def test_invalid_channel_id():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], -16, 0)
        channel_messages_v1(id4['auth_user_id'], 0, 0)
        channel_messages_v1(id4['auth_user_id'], 256, 0)
        channel_messages_v1(id4['auth_user_id'], '', 0)
        channel_messages_v1(id4['auth_user_id'], 'not_an_id', 0)

# channel_id is valid and the authorised user is not a member of the channel 
def test_user_not_authorised_to_channel():
    clear_v1()
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError):
        channel_messages_v1(id3['auth_user_id'], channel_id4['channel_id'], 0)

# No messages currently in channel
def test_no_messages():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    assert (channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], 0) == 
        {
            'messages' :[],
            'start': 0, 
            'end': -1
        }
    )

# Start is greater than the total number of messages in the channel
def test_start_gt_total_messages():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], 10)


##########################################
########### channel_join tests ###########
##########################################

# Invalid auth_user_id
def test_join_auth_user_id():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    with pytest.raises(AccessError):
        channel_join_v1(-1, channel_id2['channel_id'])
        channel_join_v1(0, channel_id2['channel_id'])
        channel_join_v1(256, channel_id2['channel_id'])
        channel_join_v1('', channel_id2['channel_id'])
        channel_join_v1('not_an_id', channel_id2['channel_id'])

# Invalid channel_id
def test_join_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')

    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], -1)
        channel_join_v1(id1['auth_user_id'], 0)
        channel_join_v1(id1['auth_user_id'], 256)
        channel_join_v1(id1['auth_user_id'], '')
        channel_join_v1(id1['auth_user_id'], 'not_an_id')

# Input error when the authorised user is already a member of the channel
def test_join_already_in(): 
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])

    with pytest.raises(InputError): 
        channel_join_v1(id2['auth_user_id'], channel_id2['channel_id'])
        channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])

# AccessError when channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
def test_join_access_error(): 
    clear_v1()
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError): 
        channel_join_v1(id3['auth_user_id'], channel_id4['channel_id'])

# Test channel_join function
def test_valid_channel_join(): 
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    
    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details1 = channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details2 = channel_details_v1(id2['auth_user_id'], channel_id2['channel_id'])
    assert details1 == details2
