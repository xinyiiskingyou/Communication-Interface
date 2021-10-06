'''
Test channels_create, channels_list and channels_list_all function
'''

import pytest
from src.channels import channels_list_v1, channels_create_v1, channels_listall_v1
from src.channel import channel_invite_v1, channel_join_v1, channel_details_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError

##########################################
######### channels_create tests ##########
##########################################

# Access Error
def test_create_auth_user_id():
    '''
    Test nvalid auth_user_id
    '''
    clear_v1()
    # Public
    with pytest.raises(AccessError):
        channels_create_v1(-16, '1531_CAMEL', True)
    with pytest.raises(AccessError):
        channels_create_v1(0, '1531_CAMEL', True)
    with pytest.raises(AccessError):
        channels_create_v1(256, '1531_CAMEL', True)
    with pytest.raises(AccessError):
        channels_create_v1('not_an_id', '1531_CAMEL', True)
    with pytest.raises(AccessError):
        channels_create_v1('', '1531_CAMEL', True)

    # Private
    with pytest.raises(AccessError):
        channels_create_v1(-16, '1531_CAMEL', False)
    with pytest.raises(AccessError):
        channels_create_v1(0, '1531_CAMEL', False)
    with pytest.raises(AccessError):
        channels_create_v1(256, '1531_CAMEL', False)
    with pytest.raises(AccessError):
        channels_create_v1('not_an_id', '1531_CAMEL', False)
    with pytest.raises(AccessError):
        channels_create_v1('', '1531_CAMEL', False)

    # invalid auth_user_id with invalid channel name
    with pytest.raises(AccessError):
        channels_create_v1(-16, ' ', False)
    with pytest.raises(AccessError):
        channels_create_v1(1, 'a' * 50, True)
    with pytest.raises(AccessError):
        channels_create_v1(11, '', False)

# InputError
def test_create_invalid_name():
    '''
    Test when length of name is less than 1 or more than 20 characters
    '''
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], '', True)
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], ' ', True)
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], '                      ', True)
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], 'a' * 21, True)
    with pytest.raises(InputError):
        channels_create_v1(id1['auth_user_id'], 'a' * 50, True)



##### Implementation #####

def test_create_valid_channel_id():
    '''
    Assert channel_id for one, two and three channels created by two different users
    '''
    clear_v1()
    auth_id1 = auth_register_v1('abc1@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v1(auth_id1['auth_user_id'], '1531_CAMEL_1', True)
    assert channel_id1['channel_id'] == 1

    channel_id2 = channels_create_v1(auth_id1['auth_user_id'], '1531_CAMEL_2', True)
    assert channel_id2['channel_id'] == 2

    auth_id2 = auth_register_v1('abc2@gmail.com', 'password', 'bfirst', 'blast')
    channel_id3 = channels_create_v1(auth_id2['auth_user_id'], '1531_CAMEL_3', True)
    assert channel_id3['channel_id'] == 3

    auth_id3 = auth_register_v1('abc3@gmail.com', 'password', 'cfirst', 'clast')
    channel_id4 = channels_create_v1(auth_id3['auth_user_id'], '1531_CAMEL_3', False)
    assert channel_id4['channel_id'] == 4

def test_negative_channel_id():
    '''
    Assert channel_id can never be a negative number
    '''
    clear_v1()
    auth_id = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v1(auth_id['auth_user_id'], '1531_CAMEL', True)
    assert channel_id1['channel_id'] > 0

#################################################
### channels_list and channels_list_all tests ###
#################################################

# Access Error
def test_list_auth_user_id():
    '''
    Test invalid auth_user_id for channels_list
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channels_list_v1(-16)
    with pytest.raises(AccessError):
        channels_list_v1(0)
    with pytest.raises(AccessError):
        channels_list_v1(256)
    with pytest.raises(AccessError):
        channels_list_v1('not_an_id')
    with pytest.raises(AccessError):
        channels_list_v1('')

# Access Error
def test_listall_invalid_auth_user_id():
    '''
    Test invalid auth_user_id for channels_listall
    '''
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1(-16)
    with pytest.raises(AccessError):
        channels_listall_v1(0)
    with pytest.raises(AccessError):
        channels_listall_v1(256)
    with pytest.raises(AccessError):
        channels_listall_v1('not_an_id')
    with pytest.raises(AccessError):
        channels_listall_v1('')


##### Implementation ######

def test_no_channels():
    '''
    Test if an authorised user that dosen't have channel
    it should return empty
    '''
    clear_v1()
    no_channel = auth_register_v1('email1@gmail.com', 'password1', 'afirst', 'alast')
    assert channels_list_v1(no_channel['auth_user_id']) == {'channels':[]}
    assert channels_listall_v1(no_channel['auth_user_id']) == {'channels':[]}
    assert channels_list_v1(no_channel['auth_user_id']) == channels_listall_v1(no_channel['auth_user_id'])

def test_channels_list():
    '''
    Test output of channels_list_function
    '''

    clear_v1()
    # test if a public channel can be appended in the list
    x_register = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
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

    assert len(channels_list_v1(x_register['auth_user_id'])['channels']) == 1
    assert len(channels_listall_v1(x_register['auth_user_id'])['channels']) == 1

    # Test if a private channel can be appended in the list
    sally_register = auth_register_v1('email2@gmail.com','comp1531', 'afirst','alast')
    sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)

    assert(channels_list_v1(sally_register['auth_user_id']) ==
        {
            'channels':[
                {
                    'channel_id': sally_channel['channel_id'],
                    'name': 'sally'
                },
            ]
        })

    assert len(channels_list_v1(sally_register['auth_user_id'])['channels']) == 1
    assert len(channels_listall_v1(sally_register['auth_user_id'])['channels']) == 2
    assert len(channels_listall_v1(x_register['auth_user_id'])['channels']) == 2

def test_channels_listall():
    '''
    Test output of channels_listall_function
    '''
    clear_v1()
    id1 = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
    id1_channel = channels_create_v1(id1['auth_user_id'], 'alpha', True)

    assert(channels_listall_v1(id1['auth_user_id']) ==
        {
            'channels':[
                {
                    'channel_id': id1_channel['channel_id'],
                    'name': 'alpha'
                }
            ]
        }
    )

def test_listall_channels():
    '''
    Test channels_list_all function
    '''
    clear_v1()
    id1 = auth_register_v1('ashley@gmail.com', 'ashpass', 'afirst', 'alast')
    id2 = auth_register_v1('ashemail@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('id3@gmail.com', 'password', 'cfirst', 'clast')
    
    id2_channel = channels_create_v1(id2['auth_user_id'], 'anna', False)
    assert(channels_list_v1(id2['auth_user_id']) ==
        {
            'channels':[
                {
                    'channel_id': id2_channel['channel_id'],
                    'name': 'anna'
                },
            ]
        })
    id1_channel_1 = channels_create_v1(id1['auth_user_id'], 'ashley', False)
    assert(channels_list_v1(id1['auth_user_id']) ==
        {
            'channels':[
                {
                    'channel_id': id1_channel_1['channel_id'],
                    'name': 'ashley'
                },
            ]
        })
    id1_channel_2 = channels_create_v1(id1['auth_user_id'], 'ash', True)
    #using channel details to fix pylint 
    assert (channel_details_v1(id1['auth_user_id'], id1_channel_2['channel_id']) == 
        {
            'name': 'ash',
            'is_public': True,
            'owner_members':[
                {
                    'u_id': 1,
                    'email': 'ashley@gmail.com',
                    'name_first': 'afirst',
                    'name_last': 'alast',
                    'handle_str': 'afirstalast'

                },
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'email': 'ashley@gmail.com',
                    'name_first': 'afirst',
                    'name_last': 'alast',
                    'handle_str': 'afirstalast'
                }
            ]
        })
    # Makes sure that listall output for all authorised users is the same
    assert len(channels_listall_v1(id1['auth_user_id'])['channels']) == 3
    assert len(channels_listall_v1(id2['auth_user_id'])['channels']) == 3
    assert len(channels_listall_v1(id3['auth_user_id'])['channels']) == 3

    assert len(channels_list_v1(id1['auth_user_id'])['channels']) == 2
    assert len(channels_list_v1(id2['auth_user_id'])['channels']) == 1
    assert len(channels_list_v1(id3['auth_user_id'])['channels']) == 0

def test_list_listall_with_invite_join():
    '''
    Tests channels_list and channels_listall with channel_invite and channel_join
    '''
    clear_v1()
    id1 = auth_register_v1('ashley@gmail.com', 'ashpass', 'afirst', 'alast')
    id2 = auth_register_v1('ashemail@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('id3@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v1('id4@gmail.com', 'password', 'dfirst', 'dlast')

    id1_channel = channels_create_v1(id1['auth_user_id'], 'anna', True)
    channel_join_v1(id2['auth_user_id'], id1_channel['channel_id'])
    channel_invite_v1(id1['auth_user_id'], id1_channel['channel_id'], id3['auth_user_id'])

    id2_channel = channels_create_v1(id2['auth_user_id'], 'id2_channel', False)
    channel_invite_v1(id2['auth_user_id'], id2_channel['channel_id'], id4['auth_user_id'])

    assert len(channels_listall_v1(id4['auth_user_id'])['channels']) == 2

    assert len(channels_list_v1(id1['auth_user_id'])['channels']) == 1
    assert len(channels_list_v1(id2['auth_user_id'])['channels']) == 2
    assert len(channels_list_v1(id3['auth_user_id'])['channels']) == 1
    assert len(channels_list_v1(id4['auth_user_id'])['channels']) == 1
