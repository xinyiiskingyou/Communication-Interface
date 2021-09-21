import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

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
        
        
# Valid email, password, first name and last name
def test_register_valid():
    clear_v1()
    register_return = auth_register_v1('abc@gmail.com', 'password', 'first_name', 'last_name')
    auth_user_id_1 = register_return['auth_user_id']

    login_return = auth_login_v1('abc@gmail.com', 'password')
    auth_user_id_2 = register_return['auth_user_id']

    assert auth_user_id_1 == auth_user_id_2