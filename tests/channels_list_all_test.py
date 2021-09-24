import pytest
from src.other import clear_v1 
from src.channels import channels_listall_v1
from src.data_store import data_store

def test_listall_channels(): 
    clear_v1()
    channels_listall_v1(123)