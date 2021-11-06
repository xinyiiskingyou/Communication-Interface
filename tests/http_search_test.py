import pytest
import requests
import json
from src import config
from tests.fixture import global_owner, register_user2, register_user3
from tests.fixture import user1_channel_message_id, create_channel, user1_send_dm, create_dm
from tests.fixture import user1_handle_str, user2_handle_str, channel1_name, dm1_name, user3_handle_str
from tests.fixture import VALID, ACCESSERROR, INPUTERROR

###############################################
############## search/v1 tests ################
###############################################

# Length of query string is less than 1 or over 1000 characters
def test_search_invalid_query_str_format(global_owner):

    user1_token = global_owner['token']
    
    search1 = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'a' * 1001
    })
    assert search1.status_code == INPUTERROR

    search2 = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': ''
    })
    assert search2.status_code == INPUTERROR

    search3 = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'a'
    })
    assert search3.status_code == VALID

    search4 = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'a' * 1000
    })
    assert search4.status_code == VALID


###### Implementation ######

# User has joined no channel/DM and there is at least one channel/DM with the query string
def test_search_not_member_of_channel_dm(global_owner, register_user2, register_user3, create_channel):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    user3_token = register_user3['token']

    # User 1 creates channel and sends message with query string
    channel1_id = create_channel['channel_id']

    send_channel_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'hello'
    })
    
    # User 1 creates DM and sends message with query string
    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': [user2_id]
    })
    dm1_id = create_dm1['dm_id']

    send_dm_message1 = requests.post(config.url + "message/senddm/v1",json = {	
        'token': user1_token,	
        'dm_id': dm1_id,	
        'message': 'hello'	
    })	

    search = requests.get(config.url + "search/v1", params = {
        'token': user3_token,
        'query_str': 'hello'
    })
    assert search.status_code == VALID
    assert (json.loads(search.text) == 
    {
        'messages': []
    })

# User is member of some of the channels/DMs but not all 
def test_search_member_of_some_channel_dm(global_owner, register_user2, register_user3, create_channel):

    user1_token = global_owner['token']
    user2_token = register_user2['token']
    user2_id = register_user2['auth_user_id']
    user3_token = register_user3['token']

    # Channels
    channel1_id = create_channel['channel_id']

    channel2 = requests.post(config.url + "channels/create/v2", json ={
        'token': user2_token,
        'name': 'barry',
        'is_public': True
    })
    channel2_id = channel2['channel_id']

    # User 2 is not member of User 1's channel
    send_channel_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'hello'
    })

    # User 2 is member of channel
    send_channel_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user2_token,
        'channel_id': channel2_id, 
        'message': 'hello'
    })
    
    # DM
    create_dm1 = requests.post(config.url + "dm/create/v1", json = {
        'token': user1_token,
        'u_ids': []
    })
    dm1_id = create_dm1['dm_id']

    create_dm2 = requests.post(config.url + "dm/create/v1", json = {
        'token': user2_token,
        'u_ids': []
    })
    dm2_id = create_dm2['dm_id']

    send_dm_message1 = requests.post(config.url + "message/senddm/v1",json = {	
        'token': user1_token,	
        'dm_id': dm1_id,	
        'message': 'hello'	
    })	

    send_dm_message2 = requests.post(config.url + "message/senddm/v1",json = {	
        'token': user2_token,	
        'dm_id': dm2_id,	
        'message': 'hello'	
    })	

    search = requests.get(config.url + "search/v1", params = {
        'token': user2_token,
        'query_str': 'hello'
    })
    assert search.status_code == VALID
    assert len(json.loads(search.text)['messages']) == 2

# Basic, one word: Query string 'hello'
# User has joined only one channel
def test_search_query_str_hello(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    # Messages 'search' picks up
    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'hello'
    })

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': ' hello   '
    })

    send_message3 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'soidhhellohsoidhs'
    })

    send_message4 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': '!@#3hello#%$'
    })

    send_message5 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': '!HELLO!'
    })

    send_message6 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': '#hElLo2'
    })

    search1 = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'hello'
    })
    assert search1.status_code == VALID
    assert len(json.loads(search1.text)['messages']) == 7

    # Messages 'search' does not pick up 
    send_message7 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'h1e1l1l1o'
    })

    send_message8 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'h e l l o'
    })

    search1 = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'hello'
    })
    assert search1.status_code == VALID
    assert len(json.loads(search1.text)['messages']) == 7

# Number: Query string '345'
# User has joined only one channel
def test_search_query_str_number(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': '345'
    })

    search = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': '345'
    })
    assert search.status_code == VALID
    assert len(json.loads(search.text)['messages']) == 1

# Multiple words: Query string 'hello there'
def test_search_query_str_multiple_words(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'Hello there!'
    })

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'hello there '
    })

    search = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'hello there'
    })
    assert search.status_code == VALID
    assert len(json.loads(search.text)['messages']) == 2

    send_message2 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': 'hello  there'
    })

    search = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': 'hello there'
    })
    assert search.status_code == VALID
    assert len(json.loads(search.text)['messages']) == 2

# Non-alphanumerical characters: Query string '!%#*{;?/<~='
def test_search_query_str_multiple_words(global_owner, create_channel):

    user1_token = global_owner['token']
    channel1_id = create_channel['channel_id']

    send_message1 = requests.post(config.url + "message/send/v1", json = {
        'token': user1_token,
        'channel_id': channel1_id, 
        'message': '!%#*{;?/<~='
    })

    search = requests.get(config.url + "search/v1", params = {
        'token': user1_token,
        'query_str': '!%#*{;?/<~='
    })
    assert search.status_code == VALID
    assert len(json.loads(search.text)['messages']) == 1