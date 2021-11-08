import time 
from src.data_store import get_data, save
from src.error import InputError, AccessError
from src.helper import check_valid_channel_id, check_valid_member_in_channel, get_channel_details, get_handle
from src.server_helper import valid_user, decode_token
from src.message import message_sendlater_v1
from datetime import datetime, timezone

def standup_start_v1(token, channel_id, length):
    '''
    <Starts a standup with the given time in seconds>

    Arguments:
        token (string)    - a user's unique token 
        channel_id (int)  - a channel's unique id 
        length (int) - the given number of seconds the user wants 
                        the standup to be 

    Exceptions:
        InputError  - Occurs when channel_id isn't valid, length number is negative or standup is   
                        currently happening 
        AccessError - Occurs when the user is not an authorised member of the channel

    Return Value:
        Returns time_finish when the time is up. 
    ''' 

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel_id does not refer to a valid channel')

    channel = get_data()['channels']
    # channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'The authorised user is not a member of the channel')

    # length is a negative integer
    if length < 0: 
        raise InputError(description = 'Length` cannot be a negative number')

    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            if channel['standup']['is_active'] == True:
                raise InputError('An active standup is currently running in the channel')
            else:
                channel['standup']['is_active'] = True
                time_finish = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + length
                channel['standup']['time_finish'] = int(time_finish)
                save()
    return {'time_finish': time_finish}

def standup_active_v1(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what time the standup finishes. 

    Arguments:
        token (string)    - a user's unique token 
        channel_id (int)  - a channel's unique id 

    Exceptions:
        InputError  - Occurs when channel_id isn't valid
        AccessError - Occurs when the user is not an authorised member of the channel

    Return Value:
        Returns if the standup is active and the time is finishes(finished)
    ''' 

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Input error when channel_id does not refer to a valid channel
    if not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel_id does not refer to a valid channel')

    # channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'The authorised user is not a member of the channel')

    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            # If no standup is active, then time_finish returns None.
            if channel['standup']['is_active'] == False:
                return {
                    'is_active': False,
                    'time_finish': None
                }

            # if standup has finished
            current_time = int(time.time())
            if channel['standup']['time_finish'] < current_time:
                return {
                    'is_active': False,
                    'time_finish': None
                }
    
        return {'is_active': True, 'time_finish': channel['standup']['time_finish']}

def standup_send_v1(token, channel_id, message): 
    '''
    Sending a message to get buffered in the standup queue, assuming a standup is currently active.

    Arguments:
        token (string)    - a user's unique token 
        channel_id (int)  - a channel's unique id 

    Exceptions:
        InputError  - Occurs when channel_id isn't valid
        AccessError - Occurs when the user is not an authorised member of the channel

    Return Value:
        Returns if the standup is active and the time is finishes(finished)
    '''  
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    
    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel_id does not refer to a valid channel')

    # channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'The authorised user is not a member of the channel')
    
    # message is over 1000 characters long
    if len(message) > 1000: 
        raise InputError(description = 'message is over 1000 characters long')
    
    # an active standup is not currently running in the channel
    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            if channel['standup']['is_active'] == False:
                raise InputError(description = 'Standup is not currently running in the channel')
            else:
                handle = get_handle(auth_user_id)
                standup_message = handle + ': ' + message
                channel['standup']['queue'] += standup_message
                save()

    return {}
