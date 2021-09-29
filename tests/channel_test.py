import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channels import channels_list_v2, channels_create_v1
from src.channel import channel_details_v1
from src.error import InputError, AccessError

# Public: Invalid channel_id 
def test_c_details_invalid_id1():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    channel_id = channels_create_v1(id1['auth_user_id'], 'anna', True)
    
    with pytest.raises(InputError):
        channel_details_v1(id1['auth_user_id'], 0)
        channel_details_v1(id1['auth_user_id'], -1)
        channel_details_v1(id1['auth_user_id'], -116)


# Private: Invalid channel_id 
def test_c_details_invalid_id2():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id = channels_create_v1(id2['auth_user_id'], 'anna', False)
    
    with pytest.raises(InputError):
        channel_details_v1(id2['auth_user_id'], 0)
        channel_details_v1(id2['auth_user_id'], -1)
        channel_details_v1(id2['auth_user_id'], -116)

# Public: Authorised user is not a memner of the channel
def test_c_details_not_member1():
    clear_v1()
    id1 = auth_register_v1('abc@gmail.com', 'password', 'name_first', 'name_last')
    id2 = auth_register_v1('email@gmail.com', 'password', 'name_first', 'name_last')
    channel_id = channels_create_v1(id2['auth_user_id'], 'anna', True)
    with pytest.raises(AccessError):
         channel_details_v1(id1['auth_user_id'], 1)

# Private: Authorised user is not a memner of the channel
def test_c_details_not_member2():
    clear_v1()
    id2 = auth_register_v1('elephant@gmail.com', 'password', 'name_first', 'name_last')
    id3 = auth_register_v1('cat@gmail.com', 'password', 'name_first', 'name_last')
    channel_id = channels_create_v1(id2['auth_user_id'], 'anna', False)
    with pytest.raises(AccessError):
         channel_details_v1(id3['auth_user_id'], 1)