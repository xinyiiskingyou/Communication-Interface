import pytest
from src.channel import channel_invite_v1
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channels import channels_create_v1
from src.auth import auth_register_v1

x_register = auth_register_v1('email@gmail.com', 'password', 'x', 'lin')
x_channel = channels_create_v1(x_register['auth_user_id'], 'x', True)
sally_register = auth_register_v1('email2@gmail.com','comp1531', 'sally','zhou')
sally_channel = channels_create_v1(sally_register['auth_user_id'], 'sally', False)

def test_invalid_channel_invite():
    clear_v1()
    with pytest.raises(InputError):
        # channel_id does not refer to a valid channel
        channel_invite_v1(x_register['auth_user_id'], 1234, x_register['u_id'])
        channel_invite_v1(sally_register['auth_user_id'], 456, sally_register['u_id'])
        #u_id does not refer to a valid user
        channel_invite_v1(x_register['auth_user_id'], x_channel['channel_id'], 'sam')
        channel_invite_v1(sally_register['auth_user_id'], sally_channel['channel_id'], 'baka')

    with pytest.raises(AccessError):
        #the authorised user is not a member of the channel
        channel_invite_v1(x_register['auth_user_id'], x_channel['channel_id'], sally_register['u_id'])
        channel_invite_v1(sally_register['auth_user_id'], sally_channel['channel_id'], x_register['u_id'])

def test_valid_channel_invite():