import pytest
from src.channels import channels_list_v1, channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError

##########################################
######### channels_create tests ##########
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

