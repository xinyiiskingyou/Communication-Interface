import pytest
from src.channels import channels_create_v2
from src.channel import channel_invite_v2, channel_removeowner_v1, channel_details_v2, channel_addowner_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v2

# invalid channel_id
def test_removeowner_invalid_channel_id():

    clear_v1()
    id1 = auth_register_v2('email@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        channel_removeowner_v1(id1['token'], -1, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(id1['token'], 0, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(id1['token'], 256, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(id1['token'], 'not_an_id', id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(id1['token'], '', id2['auth_user_id'])

# invalid u_id
def test_removeowner_invalid_u_id():

    clear_v1()
    id2 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)

    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], -16)
    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], 0)
    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], 256)
    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], '')

# u_id refers to a user who is not an owner of the channel
def test_removeowner_invalid_owner_u_id():

    clear_v1()
    id2 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id4 = auth_register_v2('cat@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    channel_invite_v2(id2['token'], channel_id2['channel_id'], id4['auth_user_id'])
    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], id4['auth_user_id'])

# u_id refers to a user who is currently the only owner of the channel
def test_removeowner_only_owner():

    clear_v1()
    id2 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    with pytest.raises(InputError):
        channel_removeowner_v1(id2['token'], channel_id2['channel_id'], id2['auth_user_id'])

# channel_id is valid and the authorised user does not have owner permissions in the channel
def test_removeowener_no_permission():

    clear_v1()
    id2 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id3 = auth_register_v2('bear@gmail.com', 'password', 'bfirst', 'blast')
    id4 = auth_register_v2('cat@gmail.com', 'password', 'cfirst', 'clast')

    channel_id2 = channels_create_v2(id2['token'], 'anna', True)
    # add id3 as an owner so it would not raise Input error for only owner of the channel
    channel_invite_v2(id2['token'], channel_id2['channel_id'], id3['auth_user_id'])
    channel_addowner_v1(id2['token'], channel_id2['channel_id'], id3['auth_user_id'])
    with pytest.raises(AccessError):    
        channel_removeowner_v1(id4['token'], channel_id2['channel_id'], id2['auth_user_id'])

# valid case
def test_remove_owner_valid():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')

    # id1 creates a channel (id1 has owner permission)
    channel_id = channels_create_v2(id1['token'], 'anna', True)
    # add id2 to the channel
    channel_invite_v2(id1['token'], channel_id['channel_id'], id2['auth_user_id'])
    # promote id2 as a owner of user1's channel
    channel_addowner_v1(id1['token'], channel_id['channel_id'], id2['auth_user_id'])
    details = channel_details_v2(id1['token'], channel_id['channel_id'])
    # it should have 2 owners in the channel now
    assert len(details['owner_members']) == 2
    # now remove id2 as a owner again
    channel_removeowner_v1(id1['token'], channel_id['channel_id'], id2['auth_user_id'])
    # it should only have 1 owner now
    assert len(details['owner_members']) == 1
