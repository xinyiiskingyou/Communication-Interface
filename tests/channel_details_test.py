'''
Test channel_details function
'''

import pytest
from src.channel import channel_invite_v2, channel_details_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.other import clear_v1

##########################################
######### channel_details tests ##########
##########################################

# Input Error when channel_id does not refer to a valid channel
def test_details_invalid_channel_id():

    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        channel_details_v2(id1['token'], -1)
    with pytest.raises(InputError):
        channel_details_v2(id1['token'], 0)
    with pytest.raises(InputError):
        channel_details_v2(id1['token'], 256)
    with pytest.raises(InputError):
        channel_details_v2(id1['token'], 'not_an_id')
    with pytest.raises(InputError):
        channel_details_v2(id1['token'], '')

# Access Error when authorised user is not a member of the channel
def test_details_not_member():

    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('cat@gmail.com', 'password1', 'cfirst', 'clast')
    channel_id = channels_create_v2(id2['token'], 'anna', True)
    channel_id1 = channels_create_v2(id3['token'], 'a', False)

    # Public
    with pytest.raises(AccessError):
        channel_details_v2(id1['token'], channel_id['channel_id'])

    # Private
    with pytest.raises(AccessError):
        channel_details_v2(id1['token'], channel_id1['channel_id'])

##### Implementation #####
def test_details_valid_channel():
    '''
    Test correct details for valid channel
    '''
    clear_v1()
    a_id = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    new_id = auth_register_v2('email@gmail.com', 'password', 'afirst', 'alast')
    channel_id = channels_create_v2(a_id['token'], 'anna', True)

    assert(channel_details_v2(a_id['token'], channel_id['channel_id']) ==
        {
        'name': 'anna',
        'is_public': True,
        'owner_members':[
            {
                'u_id': 1,
                'email': 'abc@gmail.com',
                'name_first': 'afirst',
                'name_last': 'alast',
                'handle_str': 'afirstalast'

            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'abc@gmail.com',
                'name_first': 'afirst',
                'name_last': 'alast',
                'handle_str': 'afirstalast'
            }
        ]
    })

    channel_invite_v2(a_id['token'], channel_id['channel_id'], new_id['auth_user_id'])
    len1 = len(channel_details_v2(a_id['token'], channel_id['channel_id'])['owner_members'])
    assert len1 == 1

    len2 = len(channel_details_v2(a_id['token'], channel_id['channel_id'])['all_members'])
    assert len2 == 2
