import pytest
from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

##########################################
########### auth_register tests ##########
##########################################

# Email does not have proper format
def test_register_invalid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc', 'password', 'first1', 'last1')
        auth_register_v1('abc@gmail', 'password', 'first2', 'last2')

# Duplicate email address
def test_register_duplicate_email():
    clear_v1()
    auth_register_v1('abc@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', 'password', 'bfirst', 'blast')

# Password is < 6 characters
def test_register_invalid_password():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v1('abc@gmail.com', '12345', 'afirst', 'alast')

# First and last names are either < 1 or > 50 characters in length 
def test_register_invalid_name():
    clear_v1()
    with pytest.raises(InputError):
        # Invalid first name
        auth_register_v1('abc@gmail.com', '12345', 'a' * 50, 'alast')

        # Invalid last name
        auth_register_v1('abc@gmail.com', '12345', 'bfirst', 'b' * 50)
 

##########################################
########### auth_login tests #############
##########################################

# Email tested does not belong to user 
def test_email_not_belong_user():
    clear_v1()
    auth_register_v1('correct.email@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        auth_login_v1('wrong.email@unsw.edu.au', 'password')

# Password is not correct
def test_incorrect_password():
    clear_v1()
    auth_register_v1('email@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        auth_login_v1('email@unsw.edu.au', 'wrong password')


##### Implementation for auth_register and auth_login #####
# That auth_user_id's of different emails are unique
def test_unique_auth_id():
    clear_v1()
    user1_reg = auth_register_v1('elephant@unsw.edu.au', 'password', 'afirst', 'alast')
    user2_reg = auth_register_v1('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    assert user1_reg['auth_user_id'] == 1
    assert user2_reg['auth_user_id'] == 2

# That auth reg and auth login return the same value
def test_auth_reg_and_log1():
    clear_v1()
    user1_reg = auth_register_v1('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user1_log = auth_login_v1('abc@unsw.edu.au', 'password')
    assert user1_reg['auth_user_id'] == 1
    assert user1_log['auth_user_id'] == 1


# Tests that auth_login gives the correct dictionary as output
def test_correct_auth_login_output():
    clear_v1()
    user1_reg = auth_register_v1('elephant@unsw.edu.au', 'password', 'afirst', 'alast')
    user1_log = auth_login_v1('elephant@unsw.edu.au', 'password')
    user2_reg = auth_register_v1('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    user2_log = auth_login_v1('cat@unsw.edu.au', 'password')
    assert user1_log == {'auth_user_id': 1}
    assert user2_log == {'auth_user_id': 2}

    print(auth_login_v1('cat@unsw.edu.au', 'password'))
    
