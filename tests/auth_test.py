import pytest

from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

# Email and password is valid and user is able to successfully login
def valid_email_password():
    clear_v1()
    auth_register_v1('email@unsw.edu.au', 'password', 'name_first', 'name_last')
    auth_login_v1('email@unsw.edu.au', 'password')

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



