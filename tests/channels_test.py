import pytest
from src.data_store import data_store
from src.channels import channels_create_v1
from src.error import InputError
from src.other import clear_v1
from src.auth import auth_register_v1
def test_create_invalid_name():
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, '', 1)
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, ' ', 1)
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, '                      ', 1)
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, 'abcdefghijklmlaqwertq', 1)

def test_create_valid_public():
    clear_v1()
    channels_create_v1(123, '1531_CAMEL', 1)

def test_create_valid_private():
    clear_v1()
    channels_create_v1(1, 'channel', 0)

def test_create_invalid_id():
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1('', '1531_CAMEL', 1)
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1('not_a_id', '1531_CAMEL', 1)

def test_create_invalid_public():
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, '1531_CAMEL', -1)
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, '1531_CAMEL', 100)

