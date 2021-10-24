'''
Test auth_register and auth_login function
'''

import pytest
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
from src.other import clear_v1

##########################################
########### auth_register tests ##########
##########################################

def test_register_invalid_email():
    '''
    Test invalid email format
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc', 'password', 'first1', 'last1')
    with pytest.raises(InputError):
        auth_register_v2('abc@gmail', 'password', 'first2', 'last2')

def test_register_duplicate_email():
    '''
    Test duplicate email address
    '''
    clear_v1()
    auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        auth_register_v2('abc@gmail.com', 'password', 'bfirst', 'blast')

def test_register_invalid_password():
    '''
    Test password is < 6 characters
    '''
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@gmail.com', '12345', 'afirst', 'alast')

def test_register_invalid_name():
    '''
    Test first and last names are either < 1 or > 50 characters in length
    '''
    clear_v1()
    with pytest.raises(InputError):
        # Invalid first name
        auth_register_v2('abc@gmail.com', '12345', 'a' * 50, 'alast')
    with pytest.raises(InputError):
        # Invalid last name
        auth_register_v2('abc@gmail.com', '12345', 'bfirst', 'b' * 50)

##########################################
########### auth_login tests #############
##########################################

def test_email_not_belong_user():
    '''
    Email tested does not belong to user
    '''
    clear_v1()
    auth_register_v2('correct.email@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        auth_login_v2('wrong.email@unsw.edu.au', 'password')

def test_incorrect_password():
    '''
    Test password is not correct
    '''
    clear_v1()
    auth_register_v2('email@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        auth_login_v2('email@unsw.edu.au', 'wrong password')

###########################################################
##### Implementation for auth_register and auth_login #####
###########################################################

# Register two users and log them in
clear_v1()
user1_reg = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
user1_log = auth_login_v2('abc@unsw.edu.au', 'password')

user2_reg = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
user2_log = auth_login_v2('cat@unsw.edu.au', 'password')

def test_unique_auth_id():
    '''
    Test auth_user_id's of different emails are unique
    '''
    assert user1_reg['auth_user_id'] == 1
    assert user2_reg['auth_user_id'] == 2

def test_auth_reg_and_log1():
    '''
    Test auth reg and auth login return the same value
    '''
    assert user1_reg['auth_user_id'] == 1
    assert user1_log['auth_user_id'] == 1
