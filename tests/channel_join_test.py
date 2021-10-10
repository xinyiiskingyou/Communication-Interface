import pytest
from src.channel import channel_invite_v2, channel_details_v2, channel_join_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1


##########################################
########### channel_join tests ###########
##########################################

# Invalid channel_id
def test_join_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')

    with pytest.raises(InputError):
        channel_join_v2(id1['token'], -1)
    with pytest.raises(InputError):
        channel_join_v2(id1['token'], 0)
    with pytest.raises(InputError):
        channel_join_v2(id1['token'], 256)
    with pytest.raises(InputError):
        channel_join_v2(id1['token'], 'not_an_id')
    with pytest.raises(InputError):
        channel_join_v2(id1['token'], '')

# Input error when the authorised user is already a member of the channel
def test_join_already_member(): 
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('dog@gmail.com', 'password', 'cfirst', 'clast')

    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    channel_id3 = channels_create_v2(id3['token'], 'beta', True)

    channel_join_v2(id1['token'], channel_id2['channel_id'])
    channel_invite_v2(id3['token'], channel_id3['channel_id'], id1['auth_user_id'])

    with pytest.raises(InputError): 
        channel_join_v2(id2['token'], channel_id2['channel_id'])
    with pytest.raises(InputError): 
        channel_join_v2(id1['token'], channel_id2['channel_id'])
    with pytest.raises(InputError):
        channel_join_v2(id1['token'], channel_id3['channel_id'])


# AccessError when channel_id refers to a channel that is private 
# and the authorised user is not already a channel member and is not a global owner
def test_join_priv_but_not_global_owner(): 
    clear_v1()
    id2 = auth_register_v2('cat@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('dog@gmail.com', 'password', 'cfirst', 'clast')
    channel_id2 = channels_create_v2(id2['token'], 'shelly', False)

    with pytest.raises(AccessError): 
        channel_join_v2(id3['token'], channel_id2['channel_id'])


##### Implementation #####
# Test channel_join function for joining a public channel
def test_join_valid_public_channel(): 
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('dog@gmail.com', 'password', 'cfirst', 'clast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    
    channel_join_v2(id1['token'], channel_id2['channel_id'])
    channel_join_v2(id3['token'], channel_id2['channel_id'])
    details1 = channel_details_v2(id1['token'], channel_id2['channel_id'])
    details2 = channel_details_v2(id2['token'], channel_id2['channel_id'])
    assert len(details1['all_members']) == 3
    assert len(details2['all_members']) == 3
    assert len(details1['owner_members']) == 1
    assert len(details2['owner_members']) == 1


# Test channel_join function for joining a private channel
def test_join_valid_private_channel():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', False)
    
    # Tests that global owner of Streams is able to join any private channel
    channel_join_v2(id1['token'], channel_id2['channel_id'])
    details1 = channel_details_v2(id1['token'], channel_id2['channel_id'])
    details2 = channel_details_v2(id2['token'], channel_id2['channel_id'])
    
    assert len(details1['all_members']) == 2
    assert len(details2['all_members']) == 2
    assert len(details1['owner_members']) == 1
    assert len(details2['owner_members']) == 1


# Test combination of channel_join and channel_invite
def test_join_invite_public():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('dog@gmail.com', 'coolpassword', 'cfirst', 'clast')
    channel_id1 = channels_create_v2(id1['token'], 'anna', True)

    channel_join_v2(id2['token'], channel_id1['channel_id'])
    channel_invite_v2(id2['token'], channel_id1['channel_id'], id3['auth_user_id'])
    details1 = channel_details_v2(id3['token'], channel_id1['channel_id'])
    assert len(details1['all_members']) == 3    

