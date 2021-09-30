import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_messages_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_listall_v1, channels_list_v1
from src.auth import auth_register_v1
from src.other import clear_v1

@pytest.fixture
def register_and_create_channel():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id2['auth_user_id'], 'shelly', False)

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
        channel_invite_v1(256, channel_id4['channel_id'], id4['auth_user_id'])

        #Private
        channel_invite_v1(-16, channel_id4['channel_id'], id2['auth_user_id'])
        channel_invite_v1(0, channel_id4['channel_id'], id3['auth_user_id'])
        channel_invite_v1(256, channel_id4['channel_id'], id1['auth_user_id'])

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

        # Private
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], -16)
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], 0)
        channel_invite_v1(id4['auth_user_id'], channel_id24['channel_id'], 256)



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

        #Private
        channel_details_v1(-1, channel_id4['channel_id'])
        channel_details_v1(0, channel_id4['channel_id'])
        channel_details_v1(256, channel_id4['channel_id'])

# Invalid channel_id
def test_details_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')

    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], -1)
        channel_details_v1(id1['auth_user_id'], 0)
        channel_details_v1(id1['auth_user_id'], 256)

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

        # Private
        channel_messages_v1(-16, channel_id4['channel_id'], 0)
        channel_messages_v1(0, channel_id4['channel_id'], 0)
        channel_messages_v1(256, channel_id4['channel_id'], 0)

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

# channel_id does not refer to a valid channel
def test_invalid_channel_id():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], -16, 0)
        channel_messages_v1(id4['auth_user_id'], 0, 0)
        channel_messages_v1(id4['auth_user_id'], 260, 0)

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

# AccessError Invalid auth_user_id
def test_create_auth_user_id():
    clear_v1()
    with pytest.raises(AccessError):

        # Public
        channels_create_v1(-16, '1531_CAMEL', True)
        channels_create_v1(0, '1531_CAMEL', True)
        channels_create_v1(256, '1531_CAMEL', True)
        channels_create_v1('', '1531_CAMEL', True)
        channels_create_v1('not_an_id', '1531_CAMEL', True)

        #Private
        channels_create_v1(-16, '1531_CAMEL', False)
        channels_create_v1(0, '1531_CAMEL', False)
        channels_create_v1(256, '1531_CAMEL', False)
        channels_create_v1('', '1531_CAMEL', True)
        channels_create_v1('not_an_id', '1531_CAMEL', True)

# InputError when length of name is less than 1 or more than 20 characters
def test_create_invalid_name():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], '', True)
        channels_create_v1(id1['auth_user_id'], ' ', True)
        channels_create_v1(id1['auth_user_id'], '                      ', True)
        channels_create_v1(id1['auth_user_id'], 'a' * 21, True)
        channels_create_v1(id1['auth_user_id'], 'a' * 50, True)

# InputError for setting invalid privacy
def test_create_invalid_public():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', -1)
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', 0)
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', 256)
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', '')
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', 'not_an_id')

# Test if we can create a valid public channel
# DON'T KNOW WHAT THIS IS TESTING 
def test_create_valid_public():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channels_create_v1(id1['auth_user_id'], '1531_CAMEL', True)

# Test if we can create a valid private channel
# DON'T KNOW WHAT THIS IS TESTING
def test_create_valid_private():
    clear_v1()
    id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channels_create_v1(id['auth_user_id'], 'channel', False)

# Assert channel_id would never be negative number
# DON'T KNOW WHAT TO DO
def test_create_invalid_channel_id():
    clear_v1()
    auth_id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channel_id = channels_create_v1(auth_id['auth_user_id'], '1531_CAMEL', True)
    assert channel_id != -1

#################################################
### channels_list and channels_list_all tests ###
#################################################

# AccessError Invalid auth_user_id
def test_list_auth_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        assert(channels_list_v1(-16))
        assert(channels_list_v1(0))
        assert(channels_list_v1(256))
        assert(channels_list_v1(''))
        assert(channels_list_v1('not_an_id'))

# test if an authorised user that dosen't have channel
# it should return empty
def test_no_channels():
    clear_v1()
    no_channel = auth_register_v1('email1@gmail.com', 'Password1', 'anna','duong')
    assert(channels_list_v1(no_channel['auth_user_id']) == {'channels':[]})
    assert(channels_listall_v1(no_channel['auth_user_id']) == {'channels':[]})
    assert(channels_list_v1(no_channel['auth_user_id'])) == channels_listall_v1(no_channel['auth_user_id'])

# Test channels_list_function
def test_channels_list():
    clear_v1()
    # test if a public channel can be appened in the list
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

    assert(channels_list_v1(x_register['auth_user_id'])) == channels_listall_v1(x_register['auth_user_id'])

    # test if a private channel can be appened in the list
    sally_register = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
    sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)
    assert(channels_listall_v1(sally_register['auth_user_id']) == {
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

    # Testing when a user is part of one channel but not the other -> list != list_all
    assert(channels_list_v1(sally_register['auth_user_id']) != (channels_listall_v1(sally_register['auth_user_id'])))


# Test channels_list_all function
def test_listall_channels():
    clear_v1()
    ash_register = auth_register_v1('ashley@gmail.com', 'ashpass', 'ashley', 'wong')
    a_register = auth_register_v1('ashemail@gmail.com', 'password', 'anna', 'wong')
    a_channel = channels_create_v1(a_register['auth_user_id'], 'anna', False)
    ash_channel = channels_create_v1(ash_register['auth_user_id'], 'ashley', False)
    ashv1_channel = channels_create_v1(ash_register['auth_user_id'], 'ash', True)
    assert (channels_listall_v1(ash_register['auth_user_id']) == 
        {
            'channels' :[
                {
                    'channel_id': a_channel['channel_id'],
                    'name': 'anna' 
                }, 
                {
                    'channel_id' : ash_channel['channel_id'],
                    'name' : 'ashley'
                },
                {
                    'channel_id' : ashv1_channel['channel_id'],
                    'name' : 'ash' 
                }

            ],
        })

    assert (channels_list_v1(ash_register['auth_user_id']) == 
    {
        'channels' :[ 
            {
                'channel_id' : ash_channel['channel_id'],
                'name' : 'ashley'
            },
            {
                'channel_id' : ashv1_channel['channel_id'],
                'name' : 'ash' 
            }

        ],
    })

    # Testing that listall returns all the channels regardless of auth_user_id
    assert ((channels_listall_v1(ash_register['auth_user_id'])) == (channels_listall_v1(a_register['auth_user_id'])))

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
