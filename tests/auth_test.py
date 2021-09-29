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
 

# That auth_user_id's of different emails are unique
def test_unique_auth_id():
    clear_v1()
    user1_reg = auth_register_v1('elephant@unsw.edu.au', 'password', 'name_first', 'name_last')
    user2_reg = auth_register_v1('cat@unsw.edu.au', 'password', 'name_first', 'name_last')
    assert user1_reg['auth_user_id'] != user2_reg['auth_user_id']

# That auth reg and auth login return the same value
def test_auth_reg_and_log1():
    clear_v1()
    user1_reg = auth_register_v1('abc@unsw.edu.au', 'password', 'name_first', 'name_last')
    user2_log = auth_login_v1('abc@unsw.edu.au', 'password')
    assert user1_reg['auth_user_id'] == user2_log['auth_user_id']

# That auth reg and auth login return the same value
def test_auth_reg_and_log2():
    clear_v1()
    user3_reg = auth_register_v1('email@unsw.edu.au', 'password', 'name_first', 'name_last')
    user4_log = auth_login_v1('email@unsw.edu.au', 'password')
    assert user3_reg['auth_user_id'] == user4_log['auth_user_id']

######### auth_login tests ##########
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

