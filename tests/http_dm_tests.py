import pytest
import requests
import json
from src import config
from src.other import clear_v1
from src.dm import dm_details_v1 



##########################################
#########   Dm details tests    ##########
##########################################

def test_dm_details_error_token(): 
    clear_v1()
    with pytest.raises(InputError):
        dm_messages_v1('asjasd','')

def test_dm_details_error_dm_id(): 
    clear_v1
    id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError): 
        dm_messages_v1(id1['token'], 'jasjdlak')

##add valid tests 

##########################################
#########   Dm messages tests   ##########
##########################################

def test_dm_messages_error_token(): 
    clear_v1()
    with pytest.raises(InputError):
        dm_messages_v1('asjasd','', 5)

def test_dm_messages_error_dm_id(): 
    clear_v1
    id1 = auth_register_v2('abc1@gmail.com', 'password', 'afirst', 'alast')
    with pytest.raises(InputError): 
        dm_messages_v1(id1['token'], 'jasjdlak', 5)

