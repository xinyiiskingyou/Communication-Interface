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
        channels_create_v1('not_an_id', '1531_CAMEL', True)

        #Private
        channels_create_v1(-16, '1531_CAMEL', False)
        channels_create_v1(0, '1531_CAMEL', False)
        channels_create_v1(256, '1531_CAMEL', False)
        channels_create_v1('not_an_id', '1531_CAMEL', False)

# InputError when length of name is less than 1 or more than 20 characters
def test_create_invalid_name():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    with pytest.raises(InputError):
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
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', 256)
        channels_create_v1(id1['auth_user_id'], '1531_CAMEL', 'not_an_id')


##### Implementation #####
# Assert channel_id for one, two and three channels created by two different users
def test_create_valid_channel_id():
    clear_v1()
    auth_id1 = auth_register_v1('abc1@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channel_id1 = channels_create_v1(auth_id1['auth_user_id'], '1531_CAMEL_1', True)
    assert channel_id1['channel_id'] == 1

    channel_id2 = channels_create_v1(auth_id1['auth_user_id'], '1531_CAMEL_2', True)
    assert channel_id2['channel_id'] == 2

    auth_id2 = auth_register_v1('abc2@gmail.com', 'password', 'first_name_2', 'last_name_2')
    channel_id3 = channels_create_v1(auth_id2['auth_user_id'], '1531_CAMEL_3', True)
    assert channel_id3['channel_id'] == 3
    

# Assert channel_id can never be a negative number
def test_negative_channel_id():
    clear_v1()
    auth_id = auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    channel_id1 = channels_create_v1(auth_id['auth_user_id'], '1531_CAMEL', True)
    assert channel_id1['channel_id'] > 0
    

#################################################
### channels_list and channels_list_all tests ###
#################################################

# AccessError Invalid auth_user_id
def test_list_auth_user_id():
    clear_v1()
    with pytest.raises(AccessError):
        channels_list_v1(-16)
        channels_list_v1(0)
        channels_list_v1(256)
        channels_list_v1('not_an_id')

##### Implementation ######
# Test if an authorised user that dosen't have channel
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
    # test if a public channel can be appended in the list
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

    assert(len(channels_list_v1(x_register['auth_user_id'])['channels']) == 1)
    assert(len(channels_listall_v1(x_register['auth_user_id'])['channels']) == 1)

    # Test if a private channel can be appended in the list
    sally_register = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
    sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)
    
    assert(len(channels_list_v1(sally_register['auth_user_id'])['channels']) == 1)
    assert(len(channels_listall_v1(sally_register['auth_user_id'])['channels']) == 2)
    assert(len(channels_listall_v1(x_register['auth_user_id'])['channels']) == 2)
    

# Test channels_list_all function
def test_listall_channels():
    clear_v1()
    id1 = auth_register_v1('ashley@gmail.com', 'ashpass', 'ashley', 'wong')
    id2 = auth_register_v1('ashemail@gmail.com', 'password', 'anna', 'wong')
    id3 = auth_register_v1('id3@gmail.com', 'password', 'id3', 'wong')
    id2_channel = channels_create_v1(id2['auth_user_id'], 'anna', False)
    id1_channel_1 = channels_create_v1(id1['auth_user_id'], 'ashley', False)
    id1_channel_2 = channels_create_v1(id1['auth_user_id'], 'ash', True)

    assert(len(channels_listall_v1(id1['auth_user_id'])['channels']) == 3)
    assert(len(channels_listall_v1(id2['auth_user_id'])['channels']) == 3)
    assert(len(channels_listall_v1(id3['auth_user_id'])['channels']) == 3)

    assert(len(channels_list_v1(id1['auth_user_id'])['channels']) == 2)
    assert(len(channels_list_v1(id2['auth_user_id'])['channels']) == 1)
    assert(len(channels_list_v1(id3['auth_user_id'])['channels']) == 0)

