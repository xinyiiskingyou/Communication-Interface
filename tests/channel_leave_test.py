import pytest 
from src.channel import channel_join_v2, channel_leave_v1, channel_details_v2
from src.channels import channels_create_v2
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v2

#invalid channel_id 
def test_leave_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')

    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], -16)
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], 0)
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], 256)
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], 'not_an_id')
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], '')

# not an authorised member of the channel 
def test_leave_not_member():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id4 = auth_register_v2('cat@gmail.com', 'password', 'dfirst', 'dlast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    channel_id4 = channels_create_v2(id4['token'], 'shelly', False)

    # Public
    with pytest.raises(AccessError):
        channel_leave_v1(id1['token'], channel_id2['channel_id'])
    with pytest.raises(AccessError):
        channel_leave_v1(id1['token'], channel_id2['channel_id'])

    # Private
    with pytest.raises(AccessError):
        channel_leave_v1(id3['token'], channel_id4['channel_id'])
    with pytest.raises(AccessError):
        channel_leave_v1(id3['token'], channel_id4['channel_id'])

# valid case
def test_leave_valid_public_channel(): 
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

    channel_leave_v1(id1['token'], channel_id2['channel_id'])
    channel_leave_v1(id3['token'], channel_id2['channel_id'])

    details3 = channel_details_v2(id2['token'], channel_id2['channel_id'])
    assert len(details3['all_members']) == 1
'''
def test_leave_valid_public_channel1(): 
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('dog@gmail.com', 'password', 'cfirst', 'clast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    
    channel_join_v2(id1['token'], channel_id2['channel_id'])
    channel_join_v2(id3['token'], channel_id2['channel_id'])
    details = channel_details_v2(id2['token'], channel_id2['channel_id'])
    assert len(details['owner_members']) == 1
    assert len(details['all_members']) == 3

    # the only owner leaves the channel
    channel_leave_v1(id2['token'], channel_id2['channel_id'])
    assert len(details['owner_members']) == 0
    assert len(details['all_members']) == 2
'''