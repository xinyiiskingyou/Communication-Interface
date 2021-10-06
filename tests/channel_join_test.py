import pytest
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1


##########################################
########### channel_join tests ###########
##########################################

# Invalid auth_user_id
def test_join_invalid_auth_user_id():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)

    with pytest.raises(AccessError):
        channel_join_v1(-1, channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1(0, channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1(256, channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1('not_an_id', channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_join_v1('', channel_id2['channel_id'])
        

# Invalid channel_id
def test_join_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')

    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], -1)
    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], 0)
    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], 256)
    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], '')


# Invalid auth_user_id and invalid channel_id
# Raises Access Error as both Access and Input Errors are raised
def test_join_invalid_auth_user_id_and_channel_id():
    clear_v1()

    with pytest.raises(AccessError):
        channel_join_v1('', -16)
    with pytest.raises(AccessError):
        channel_join_v1('not_an_id', 0)
    with pytest.raises(AccessError):
        channel_join_v1(256, 256)
    with pytest.raises(AccessError):
        channel_join_v1(0, 'not_an_id')
    with pytest.raises(AccessError):
        channel_join_v1(-16, '')


# Input error when the authorised user is already a member of the channel
def test_join_already_member(): 
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('dog@gmail.com', 'password', 'cfirst', 'clast')

    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id3 = channels_create_v1(id3['auth_user_id'], 'beta', True)

    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    channel_invite_v1(id3['auth_user_id'], channel_id3['channel_id'], id1['auth_user_id'])

    with pytest.raises(InputError): 
        channel_join_v1(id2['auth_user_id'], channel_id2['channel_id'])
    with pytest.raises(InputError): 
        channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    with pytest.raises(InputError):
        channel_join_v1(id1['auth_user_id'], channel_id3['channel_id'])


# AccessError when channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
def test_join_priv_but_not_global_owner(): 
    clear_v1()
    id2 = auth_register_v1('cat@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('dog@gmail.com', 'password', 'cfirst', 'clast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError): 
        channel_join_v1(id3['auth_user_id'], channel_id2['channel_id'])


##### Implementation #####
# Test channel_join function for joining a public channel
def test_join_valid_public_channel(): 
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('dog@gmail.com', 'password', 'cfirst', 'clast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    
    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    channel_join_v1(id3['auth_user_id'], channel_id2['channel_id'])
    details1 = channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details2 = channel_details_v1(id2['auth_user_id'], channel_id2['channel_id'])
    assert len(details1['all_members']) == 3
    assert len(details2['all_members']) == 3
    assert len(details1['owner_members']) == 1
    assert len(details2['owner_members']) == 1


# Test channel_join function for joining a private channel
def test_join_valid_private_channel():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', False)
    
    # Tests that global owner of Streams is able to join any private channel
    channel_join_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details1 = channel_details_v1(id1['auth_user_id'], channel_id2['channel_id'])
    details2 = channel_details_v1(id2['auth_user_id'], channel_id2['channel_id'])
    
    assert len(details1['all_members']) == 2
    assert len(details2['all_members']) == 2
    assert len(details1['owner_members']) == 1
    assert len(details2['owner_members']) == 1


# Test combination of channel_join and channel_invite
def test_join_invite_public():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v1('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v1('dog@gmail.com', 'coolpassword', 'cfirst', 'clast')
    channel_id1 = channels_create_v1(id1['auth_user_id'], 'anna', True)

    channel_join_v1(id2['auth_user_id'], channel_id1['channel_id'])
    channel_invite_v1(id2['auth_user_id'], channel_id1['channel_id'], id3['auth_user_id'])
    details1 = channel_details_v1(id3['auth_user_id'], channel_id1['channel_id'])
    assert len(details1['all_members']) == 3    

