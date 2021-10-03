import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1


##########################################
########## channel_invite tests ##########
##########################################

# Invalid auth_user_id
def test_invite_invalid_auth_user_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    # Public
    with pytest.raises(AccessError):
        channel_invite_v1(-16, channel_id2['channel_id'], id1['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(0, channel_id2['channel_id'], id3['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(256, channel_id2['channel_id'], id4['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', channel_id2['channel_id'], id4['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('', channel_id2['channel_id'], id4['auth_user_id'])

    # Private
    with pytest.raises(AccessError):
        channel_invite_v1(-16, channel_id4['channel_id'], id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(0, channel_id4['channel_id'], id3['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(256, channel_id4['channel_id'], id1['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', channel_id4['channel_id'], id3['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('', channel_id4['channel_id'], id2['auth_user_id'])


# Invalid u_id
def test_invite_invalid_u_id():
    clear_v1()
    id2 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    # Public 
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], -16)
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], 0)
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], 256)
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], '')

    # Private
    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], -16)
    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], 0)
    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], 256)
    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], '')


# Invalid channel_id
def test_invite_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], -16, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], 0, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], 256, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], 'not_an_id', id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], '', id2['auth_user_id'])


# Public: u_id refers to a user who is already a member of the channel
def test_invite_already_member_pub():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst','blast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'cfirst', 'clast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    
    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    channel_join_v1(id3['auth_user_id'], channel_id2['channel_id'])

    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], id1['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], id3['auth_user_id'])
    
    # When someone tries to invite owner
    with pytest.raises(InputError):
        channel_invite_v1(id1['auth_user_id'], channel_id2['channel_id'], id2['auth_user_id'])


# Private: u_id refers to a user who is already a member of the channel
def test_invite_already_member_priv():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'cfirst', 'clast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id1['auth_user_id'])
    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])

    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id1['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])
    
    # When someone tries to invite owner
    with pytest.raises(InputError):
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], id4['auth_user_id'])


# Authorised user is not a member of the channel
def test_invite_not_member():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    # Public
    with pytest.raises(AccessError):
        channel_invite_v1(id1['auth_user_id'], channel_id2['channel_id'], id3['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(id1['auth_user_id'], channel_id2['channel_id'], id4['auth_user_id'])

    # Private
    with pytest.raises(AccessError):
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], id1['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])


# AccessError when invalid auth_user_id and invalid channel_id
def test_invite_invalid_auth_and_invalid_channel_id(): 
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
  
    with pytest.raises(AccessError):
        channel_invite_v1('', -16, id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', 0, id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(256, 256, id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(0, 'not_an_id', id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(-16, '', id2['auth_user_id'])


# AccessError when invalid auth_user_id
# and the u_id refers to a user who is already a member of the channel
def test_invite_invalid_auth_and_u_id_already_member(): 
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)
    
    # Public 
    with pytest.raises(AccessError):
        channel_invite_v1('', channel_id2['channel_id'], id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', channel_id2['channel_id'], id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(256, channel_id2['channel_id'], id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(0, channel_id2['channel_id'], id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(-16, channel_id2['channel_id'], id2['auth_user_id'])

    # Private
    with pytest.raises(AccessError):
        channel_invite_v1('', channel_id4['channel_id'], id4['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', channel_id4['channel_id'], id4['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(256, channel_id4['channel_id'], id4['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(0, channel_id4['channel_id'], id4['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(-16, channel_id4['channel_id'], id4['auth_user_id'])


# AccessError when invalid auth_user_id
# and the u_id does not refer to a valid user
def test_invite_invalid_auth_and_invalid_u_id(): 
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)
    
    # Public 
    with pytest.raises(AccessError):
        channel_invite_v1('', channel_id2['channel_id'], -16)
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', channel_id2['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_invite_v1(256, channel_id2['channel_id'], 256)
    with pytest.raises(AccessError):
        channel_invite_v1(0, channel_id2['channel_id'], 'not_an_id')
    with pytest.raises(AccessError):
        channel_invite_v1(-16, channel_id2['channel_id'], '')

    # Private
    with pytest.raises(AccessError):
        channel_invite_v1('', channel_id4['channel_id'], -16)
    with pytest.raises(AccessError):
        channel_invite_v1('not_an_id', channel_id4['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_invite_v1(256, channel_id4['channel_id'], 256)
    with pytest.raises(AccessError):
        channel_invite_v1(0, channel_id4['channel_id'], 'not_an_id')
    with pytest.raises(AccessError):
        channel_invite_v1(-16, channel_id4['channel_id'], '')


# AccessError when channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
# and the u_id does not refer to a valid user
def test_invite_auth_not_member_and_invalid_u_id(): 
    clear_v1()
    id1 = auth_register_v1('abcd@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    # Private
    with pytest.raises(AccessError):
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], -16)
    with pytest.raises(AccessError):
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_invite_v1(id2['auth_user_id'], channel_id4['channel_id'], 256)
    with pytest.raises(AccessError):
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], 'not_an_id')
    with pytest.raises(AccessError):
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], '')


# AccessError when channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
# and the u_id refers to a user who is already a member of the channel
def test_invite_auth_not_member_and_u_id_already_member(): 
    clear_v1()
    id1 = auth_register_v1('abcd@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)
    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])

    # Private
    with pytest.raises(AccessError):
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])
    with pytest.raises(AccessError):
        channel_invite_v1(id3['auth_user_id'], channel_id4['channel_id'], id4['auth_user_id'])


##### Implementation #####
# Public: Test channel_invite function
def test_valid_channel_invite_pub(): 
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    channel_invite_v1(id2['auth_user_id'], channel_id2['channel_id'], id1['auth_user_id'])
    details1 = channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details2 = channel_details_v1(id2['auth_user_id'], channel_id2['channel_id'])
    assert len(details1['all_members']) == 2
    assert len(details2['all_members']) == 2
    assert len(details1['owner_members']) == 1
    assert len(details2['owner_members']) == 1


# Private: Test channel_invite function
def test_valid_channel_invite_priv(): 
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'bfirst', 'blast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'cfirst', 'clast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id3['auth_user_id'])
    channel_invite_v1(id4['auth_user_id'], channel_id4['channel_id'], id2['auth_user_id'])
    details3 = channel_details_v1(id3['auth_user_id'], channel_id4['channel_id'])
    details4 = channel_details_v1(id4['auth_user_id'], channel_id4['channel_id'])
    assert len(details3['all_members']) == 3
    assert len(details4['all_members']) == 3
    assert len(details3['owner_members']) == 1
    assert len(details4['owner_members']) == 1