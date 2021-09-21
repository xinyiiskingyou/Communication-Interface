import pytest

from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

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


# User has not registered with their email
def test_unregistered_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('unregistered.email@unsw.edu.au', 'password')


