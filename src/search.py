'''
Search implementation
'''

from src.data_store import get_data
from src.error import InputError, AccessError
from src.helper import check_valid_message
from src.server_helper import decode_token, valid_user
from src.channels import channels_list_v2
from src.dm import dm_list_v1


def search_v1(token, query_str):
    '''
    Given a query string, return a collection of messages in 
    all of the channels/DMs that the user has joined that contain the query.

    Arguments:
        token       (<string>)        - a user's unique token 
        query_str   (<string>)        - a string that user wants to search
        ...

    Exceptions:
        InputError  - Occurs when length of query_str is less than 1 or over 1000 characters 
        AccessError - Occurs when token is invalid

    Return Value:
        { messages }
    '''
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    # Check length of query string is less than 1 or over 1000 characters
    if not check_valid_message(query_str):
        raise InputError(description="Invalid query string format of less than 1 or over 1000 characters.")

    messages_search_list = []

    channel_list = channels_list_v2(token)

    for member_channel in channel_list['channels']:
        for test_channel in get_data()['channels']:
            if member_channel['channel_id'] == test_channel['channel_id']:
                for message_channel in test_channel['messages']:
                    if query_str.lower() in message_channel['message'].lower():
                        messages_search_list.append(message_channel)
    
    dm_list = dm_list_v1(token)

    for member_dm in dm_list['dms']:
        for test_dm in get_data()['dms']:
            if member_dm['dm_id'] == test_dm['dm_id']:
                for message_dm in test_dm['messages']:
                    if query_str.lower() in message_dm['message'].lower():
                        messages_search_list.append(message_dm)

    return {
        'messages': messages_search_list
    }


