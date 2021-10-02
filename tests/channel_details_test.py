import pytest
from src.channel import channel_invite_v1, channel_details_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1


##########################################
######### channel_details tests ##########
##########################################

# Invalid auth_user_id
def test_details_invalid_auth_user_id():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)


    # Public
    with pytest.raises(AccessError):
        channel_details_v1(-1, channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(0, channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(256, channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1('not_an_id', channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1('', channel_id2['channel_id'])


    # Private
    with pytest.raises(AccessError):
        channel_details_v1(-1, channel_id4['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(0, channel_id4['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(256, channel_id4['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1('not_an_id', channel_id4['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1('', channel_id4['channel_id'])

# Invalid channel_id
def test_details_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v1(id1['auth_user_id'], 'anna', True)

    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], -1)
    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], 0)
    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], 256)
    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], '')


# Invalid auth_user_id and invalid channel_id
# Raises Access Error as both Input and Access error are raised
def test_details_invalid_auth_user_id_and_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v1(id1['auth_user_id'], 'anna', True)

    with pytest.raises(AccessError):
        channel_details_v1('', -16)
    with pytest.raises(AccessError):
        channel_details_v1('not_an_id', 0)
    with pytest.raises(AccessError):
        channel_details_v1(256, 256)
    with pytest.raises(AccessError):
        channel_details_v1(0, 'not_an_id')
    with pytest.raises(AccessError):
        channel_details_v1(-16, '')


# Authorised user is not a member of the channel
def test_details_not_member():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    # Public
    with pytest.raises(AccessError):
        channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(id4['auth_user_id'], channel_id2['channel_id'])

    # Private
    with pytest.raises(AccessError):
        channel_details_v1(id2['auth_user_id'], channel_id4['channel_id'])
    with pytest.raises(AccessError):
        channel_details_v1(id3['auth_user_id'], channel_id4['channel_id'])



##### Implementation #####
def test_details_valid_channel():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
    channel_id1 = channels_create_v1(id1['auth_user_id'], 'anna', True)
    channel_invite_v1(id1['auth_user_id'], channel_id1['channel_id'], id2['auth_user_id'])
    assert(channel_details_v1(id1['auth_user_id'], channel_id1['channel_id']) ==
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
            }, 
            {
                'u_id': 2,
                'email': 'email@gmail.com',
                'name_first': 'afirst',
                'name_last': 'alast',
                'handle_str': 'afirstalast0'
            }
        ]
    })