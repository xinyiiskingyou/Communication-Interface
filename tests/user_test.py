import pytest
from src.user import user_profile_setemail_v1, user_profile_sethandle_v1
from src.auth import auth_register_v2, auth_login_v2
from src.helper import channels_user_details
from src.error import InputError
from src.other import clear_v1

##########################################
##### user_profile_set_email tests #######
##########################################

# Input Error when email entered is not a valid email
def user_set_email_invalid_email():
    clear_v1()
    user1 = auth_register_v2('unsw@gmail.com', 'password', 'first1', 'last1')
    with pytest.raises(InputError):
        user_profile_setemail_v1(user1['token'], 'abc')
    with pytest.raises(InputError):
        user_profile_setemail_v1(user1['token'], '123.com')

# email address is already being used by another user
def user_set_email_duplicate_email():
    clear_v1()
    user1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@gmail.com', 'password', 'bfirst', 'blast')

    with pytest.raises(InputError): 
        user_profile_setemail_v1(user1['token'], 'cat@gmail.com')
    with pytest.raises(InputError): 
        user_profile_setemail_v1(user2['token'], 'abc@gmail.com')

# valid case
def user_set_email_valid():
    clear_v1()
    user1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    user_profile_setemail_v1(user1['token'], 'comp1531@gmail.com')

    # test if user can login with new email address
    auth_login_v2('comp1531@gmail.com', 'password')

    assert user1['auth_user_id'] == auth_login_v2['auth_user_id']

##########################################
##### user_profile_set_handle tests ######
##########################################

# length of handle_str is not between 3 and 20 characters inclusive
def user_set_handle_invalid_length():
    clear_v1()
    user1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], '')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], '1')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'a1')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'a' * 22)

# handle_str contains characters that are not alphanumeric
def user_set_handle_non_alphanumeric():
    clear_v1()
    user1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], '_______===++')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], '____123-+')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], '___ad31__=]\++')

# the handle is already used by another user
def user_set_handle_already_used():
    clear_v1()
    user1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@gmail.com', 'password', 'afirst', 'alast')
    user_profile_sethandle_v1(user2['token'], 'anna')
    with pytest.raises(InputError):
        user_profile_sethandle_v1(user1['token'], 'anna')

# valid case
def user_set_handle_valid():
    clear_v1()
    user1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    user_profile_sethandle_v1(user1['token'], 'anna')
    user1_detail = channels_user_details(user1['auth_user_id'])
    assert user1_detail['handle_str'] == 'anna'
