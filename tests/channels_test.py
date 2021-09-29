import pytest
from src.channels import channels_list_v2, channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError

##########################################
######### channels_create tests ##########
##########################################

# InputError when length of name is less than 1 or more than 20 characters
def test_create_invalid_name():
    clear_v1()
    id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    with pytest.raises(InputError):
        channels_create_v1(id['auth_user_id'], '', True)
        channels_create_v1(id['auth_user_id'], ' ', True)
        channels_create_v1(id['auth_user_id'], '                      ', True)
        channels_create_v1(id['auth_user_id'], 'abcdefghijklmlaqwertq', True)

# Access error when the user doesn't have a valid auth_user_id
def test_create_invalid_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_create_v1('', '1531_CAMEL', True)
        channels_create_v1('not_a_id', '1531_CAMEL', True)

# Input error for setting invalid privacy
def test_create_invalid_public():
    clear_v1()
    id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    with pytest.raises(InputError):
        channels_create_v1(id['auth_user_id'], '1531_CAMEL', -1)
        channels_create_v1(id['auth_user_id'], '1531_CAMEL', 100)

# Test if we can create a valid public channel
def test_create_valid_public():
    clear_v1()
    id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channels_create_v1(id['auth_user_id'], '1531_CAMEL', True)

# Test if we can create a valid private channel
def test_create_valid_private():
    clear_v1()
    id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channels_create_v1(id['auth_user_id'], 'channel', False)

# Assert channel_id would never be negative number
def test_create_invalid_channel_id():
    clear_v1()
    auth_id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channel_id = channels_create_v1(auth_id['auth_user_id'], '1531_CAMEL', 0)
    assert channel_id != -1


#################################################
### channels_list and channels_list_all tests ###
#################################################

# test if a user is authorised but dosen't have channel
# it should return empty
def test_no_channels():
	clear_v1()
	no_channel = auth_register_v1('email1@gmail.com', 'Password1', 'anna','duong')
	assert(channels_list_v2(no_channel['auth_user_id']) == {'channels':[]})
	assert(channels_listall_v1(no_channel['auth_user_id']) == {'channels':[]})
	assert(channels_list_v2(no_channel['auth_user_id'])) == channels_listall_v1(no_channel['auth_user_id'])

# Test channels_list_function
def test_channels_list():

    clear_v1()
    # test if public channel can be appened in the list
    x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
    x_channel = channels_create_v1(x_register['auth_user_id'], 'x', True)
    assert(channels_list_v2(x_register['auth_user_id']) ==
        {
        'channels':[
        {
            'channel_id': x_channel['channel_id'],
            'name': 'x'
        },
        ]
    })

    assert(channels_list_v2(x_register['auth_user_id'])) == channels_listall_v1(x_register['auth_user_id'])

    # test if private channel can be appened in the list
    sally_register = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
    sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)
    assert(channels_list_v2(sally_register['auth_user_id']) == {
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

    assert(channels_list_v2(sally_register['auth_user_id']) == (channels_listall_v1(sally_register['auth_user_id'])))


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

    assert ((channels_listall_v1(ash_register['auth_user_id']))== (channels_list_v2(ash_register['auth_user_id'])))

