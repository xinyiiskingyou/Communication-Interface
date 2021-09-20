import pytest
from src.other import clear_v1
from src.channels import channels_create_v1
from src.error import InputError
def test_create_invalid():
    clear_v1()
    with pytest.raises(InputError):
        channels_create_v1(123, '', 1)
        channels_create_v1(123, 'abcdefghijklmlaqwertq', 1)

def test_create_valid():
    clear_v1()
    channels_create_v1(123, '1531_CAMEL', 1)

def test_create_invalid_id():
    clear_v1()
    channels_create_v1('123', '1531_CAMEL', 1)

def test_create_invalid_public()
    clear_v1()
    channels_create_v1(123, '1531_CAMEL', -1)