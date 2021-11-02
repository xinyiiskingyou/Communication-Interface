from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.helper import check_valid_channel_id
import threading 
import time 


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




    return time_finish 




def standup_active_v1(token, channel_id):
        '''
    <Gives the status of the standup as well as the time it will finish>

    Arguments:
        token (string)    - a user's unique token 
        channel_id (int)  - a channel's unique id 

    Exceptions:
        InputError  - Occurs when channel_id isn't valid
        AccessError - Occurs when the user is not an authorised member of the channel

    Return Value:
        Returns if the standup is active and the time is finishes(finished)
    '''  
    return {is_active, time_finish}



def standup_send_v1(token, channel_id, message): 
            '''
    <takes the messages sent during the standup and queues them 
        once the timer is up, compiles the messaages into a single message
        and sent by the user who started the standup >

    Arguments:
        token (string)    - a user's unique token 
        channel_id (int)  - a channel's unique id 

    Exceptions:
        InputError  - Occurs when channel_id isn't valid
        AccessError - Occurs when the user is not an authorised member of the channel

    Return Value:
        Returns if the standup is active and the time is finishes(finished)
    '''  
    return {}