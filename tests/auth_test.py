import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

######### auth_register tests ##########
# Email does not have proper format
def test_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc', 'password', 'first_name', 'last_name')
        auth_register_v1('abc@gmail', 'password', 'first_name', 'last_name')
        auth_register_v1('ab_c@gmail.com', 'password', 'first_name', 'last_name')
        auth_register_v1('ABC@gmail.com', 'password', 'first_name', 'last_name')


# Duplicate email address
def test_register_duplicate_email():
    clear_v1()
    auth_register_v1('abc@gmail.com', 'password', 'first_name_1', 'last_name_1')
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'first_name_2', 'last_name_2')

# Password is < 6 characters
def test_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', '12345', 'first_name', 'last_name')

# First and last names are either < 1 or > 50 characters in length 
def test_register_invalid_name():
    clear_v1()
    with pytest.raises(InputError):
        # Invalid first name
        auth_register_v1('abc@gmail.com', 'password', '', 'last_name')
        auth_register_v1('abc@gmail.com', '12345', 'a' * 50, 'last_name')

        # Invalid last name
        auth_register_v1('abc@gmail.com', 'password', 'first_name', '')
        auth_register_v1('abc@gmail.com', '12345', 'first_name', 'a' * 50)
 

######### auth_login tests ##########
# Testing different auth_user_id
def unique_auth_user_id():
    user1_reg = auth_register_v1('email@unsw.edu.au', 'password', 'name_first', 'name_last')
    user2_reg = auth_register_v1('abc@unsw.edu.au', 'password', 'name_first', 'name_last')

    user1_log = auth_login_v1('email@unsw.edu.au', 'password')
    user2_log = auth_login_v1('abc@unsw.edu.au', 'password')

    assert user1_reg != user2_reg
    assert user1_log != user2_log
    assert user1_reg == user1_log
    assert user2_reg == user2_log

# Email and password is valid and user is able to successfully login
def valid_email_password():
    clear_v1()
    user_id_register = auth_register_v1('email@unsw.edu.au', 'password', 'name_first', 'name_last')
    user_id_login = auth_login_v1('email@unsw.edu.au', 'password')
    assert user_id_register == user_id_login


# Email tested does not belong to user 
def test_email_not_belong_user():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('correct.email@unsw.edu.au', 'password', 'name_first', 'name_last')
        auth_login_v1('wrong.email@unsw.edu.au', 'password')

# Password is not correct
def test_incorrect_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('email@unsw.edu.au', 'password', 'name_first', 'name_last')
        auth_login_v1('email@unsw.edu.au', 'wrong password')

