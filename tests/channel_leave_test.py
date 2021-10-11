import pytest 
from src.channel import channel_join_v2, channel_leave_v1
from src.channels import channels_create_v2
from src.error import AccessError, InputError
from src.other import clear_v1
from src.auth import auth_register_v2


#invalid channel_id 
def test_leave_invalid_channel_id():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')

    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], -16, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], 0, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], 256, id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], 'not_an_id', id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_leave_v1(id1['token'], '', id2['auth_user_id'])

#not an authorised member of the channel 
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
        channel_leave_v1(id1['token'], channel_id2['channel_id'], id3['auth_user_id'])
    with pytest.raises(AccessError):
        channel_leave_v1(id1['token'], channel_id2['channel_id'], id4['auth_user_id'])

    # Private
    with pytest.raises(AccessError):
        channel_leave_v1(id3['token'], channel_id4['channel_id'], id1['auth_user_id'])
    with pytest.raises(AccessError):
        channel_leave_v1(id3['token'], channel_id4['channel_id'], id2['auth_user_id'])

