'''
Test channels_create, channels_list and channels_list_all function
'''

import pytest
from src.channels import channels_list_v2, channels_create_v2, channels_listall_v2
from src.channel import channel_invite_v2, channel_join_v2, channel_details_v2
from src.auth import auth_register_v2
from src.other import clear_v1
from src.error import InputError

##########################################
######### channels_create tests ##########
##########################################

# InputError
def test_create_invalid_name():
    '''
    Test when length of name is less than 1 or more than 20 characters
    '''
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        channels_create_v2(id1['token'], '', True)
    with pytest.raises(InputError):
        channels_create_v2(id1['token'], ' ', True)
    with pytest.raises(InputError):
        channels_create_v2(id1['token'], '                      ', True)
    with pytest.raises(InputError):
        channels_create_v2(id1['token'], 'a' * 21, True)
    with pytest.raises(InputError):
        channels_create_v2(id1['token'], 'a' * 50, True)



##### Implementation #####

def test_create_valid_channel_id():
    '''
    Assert channel_id for one, two and three channels created by two different users
    '''
    clear_v1()
    auth_id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v2(auth_id1['token'], '1531_CAMEL_1', True)
    assert channel_id1['channel_id'] == 1

    channel_id2 = channels_create_v2(auth_id1['token'], '1531_CAMEL_2', True)
    assert channel_id2['channel_id'] == 2

    auth_id2 = auth_register_v2('abc2@gmail.com', 'password', 'bfirst', 'blast')
    channel_id3 = channels_create_v2(auth_id2['token'], '1531_CAMEL_3', True)
    assert channel_id3['channel_id'] == 3

    auth_id3 = auth_register_v2('abc3@gmail.com', 'password', 'cfirst', 'clast')
    channel_id4 = channels_create_v2(auth_id3['token'], '1531_CAMEL_3', False)
    assert channel_id4['channel_id'] == 4

def test_negative_channel_id():
    '''
    Assert channel_id can never be a negative number
    '''
    clear_v1()
    auth_id = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v2(auth_id['token'], '1531_CAMEL', True)
    assert channel_id1['channel_id'] > 0

#################################################
### channels_list and channels_list_all tests ###
#################################################


##### Implementation ######

def test_no_channels():
    '''
    Test if an authorised user that dosen't have channel
    it should return empty
    '''
    clear_v1()
    no_channel = auth_register_v2('email1@gmail.com', 'password1', 'afirst', 'alast')
    assert channels_list_v2(no_channel['token']) == {'channels':[]}
    assert channels_listall_v2(no_channel['token']) == {'channels':[]}
    assert channels_list_v2(no_channel['token']) == channels_listall_v2(no_channel['token'])

def test_channels_list():
    '''
    Test output of channels_list_function
    '''

    clear_v1()
    # test if a public channel can be appended in the list
    x_register = auth_register_v2('email@gmail.com', 'password', 'afirst', 'alast')
    x_channel = channels_create_v2(x_register['token'], 'x', True)
    assert(channels_list_v2(x_register['token']) ==
        {
            'channels':[
                {
                    'channel_id': x_channel['channel_id'],
                    'name': 'x'
                },
            ]
        })

    assert len(channels_list_v2(x_register['token'])['channels']) == 1
    assert len(channels_listall_v2(x_register['token'])['channels']) == 1

    # Test if a private channel can be appended in the list
    sally_register = auth_register_v2('email2@gmail.com','comp1531', 'afirst','alast')
    sally_channel = channels_create_v2(sally_register['token'], 'sally', False)

    assert(channels_list_v2(sally_register['token']) ==
        {
            'channels':[
                {
                    'channel_id': sally_channel['channel_id'],
                    'name': 'sally'
                },
            ]
        })

    assert len(channels_list_v2(sally_register['token'])['channels']) == 1
    assert len(channels_listall_v2(sally_register['token'])['channels']) == 2
    assert len(channels_listall_v2(x_register['token'])['channels']) == 2

def test_channels_listall():
    '''
    Test output of channels_listall_function
    '''
    clear_v1()
    id1 = auth_register_v2('email@gmail.com', 'password', 'afirst', 'alast')
    id1_channel = channels_create_v2(id1['token'], 'alpha', True)

    assert(channels_listall_v2(id1['token']) ==
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
    id1 = auth_register_v2('ashley@gmail.com', 'ashpass', 'afirst', 'alast')
    id2 = auth_register_v2('ashemail@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('id3@gmail.com', 'password', 'cfirst', 'clast')
    
    id2_channel = channels_create_v2(id2['token'], 'anna', False)
    assert(channels_list_v2(id2['token']) ==
        {
            'channels':[
                {
                    'channel_id': id2_channel['channel_id'],
                    'name': 'anna'
                },
            ]
        })

    id1_channel_1 = channels_create_v2(id1['token'], 'ashley', False)
    assert(channels_list_v2(id1['token']) ==
        {
            'channels':[
                {
                    'channel_id': id1_channel_1['channel_id'],
                    'name': 'ashley'
                },
            ]
        })

    id1_channel_2 = channels_create_v2(id1['token'], 'ash', True)
    #using channel details to fix pylint 
    assert (channel_details_v2(id1['token'], id1_channel_2['channel_id']) == 
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
    assert len(channels_listall_v2(id1['token'])['channels']) == 3
    assert len(channels_listall_v2(id2['token'])['channels']) == 3
    assert len(channels_listall_v2(id3['token'])['channels']) == 3

    assert len(channels_list_v2(id1['token'])['channels']) == 2
    assert len(channels_list_v2(id2['token'])['channels']) == 1
    assert len(channels_list_v2(id3['token'])['channels']) == 0

def test_list_listall_with_invite_join():
    '''
    Tests channels_list and channels_listall with channel_invite and channel_join
    '''
    clear_v1()
    id1 = auth_register_v2('ashley@gmail.com', 'ashpass', 'afirst', 'alast')
    id2 = auth_register_v2('ashemail@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('id3@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v2('id4@gmail.com', 'password', 'dfirst', 'dlast')

    id1_channel = channels_create_v2(id1['token'], 'anna', True)
    channel_join_v2(id2['token'], id1_channel['channel_id'])
    channel_invite_v2(id1['token'], id1_channel['channel_id'], id3['auth_user_id'])

    id2_channel = channels_create_v2(id2['token'], 'id2_channel', False)
    channel_invite_v2(id2['token'], id2_channel['channel_id'], id4['auth_user_id'])

    assert len(channels_listall_v2(id4['token'])['channels']) == 2

    assert len(channels_list_v2(id1['token'])['channels']) == 1
    assert len(channels_list_v2(id2['token'])['channels']) == 2
    assert len(channels_list_v2(id3['token'])['channels']) == 1
    assert len(channels_list_v2(id4['token'])['channels']) == 1
