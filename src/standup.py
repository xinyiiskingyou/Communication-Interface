from src.error import InputError, AccessError
from src.auth import auth_register_v2
from src.helper import check_valid_channel_id
from src.server_helper import valid_user, decode_token
import threading 
import time 
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
    
    if length < 0: 
        raise InputError(description = 'Length` cannot be a negative number')
    
    for user in get_data()['users']: 
        if user['u_id'] = auth_user_id: 
            channel['standup']['u_id_start'] = user
    
     for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id: 
            time_finish = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + length
            t1 = threading.Thread(target = thread_helper, arg[length, auth_user_id, channel_id])
            t1.daemon = True
            channel['standup']['standup_active'] = True
            t1.start()
            channel['standup']['time_finished'] = time_finish
            return {'time_finish': time_finish

            

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

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel_id does not refer to a valid channel')

    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            is_active = channel['standup']['standup_active']
            time_finish = channel['standup']['time_finished']

            


    return {is_active, time_finish}

###can process them in here### and then send them through a thread 
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
    # queue  = [] 
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel_id does not refer to a valid channel')

    if len(message) > 1000: 
        raise InputError(description = 'message is over 1000 characters long')

    if standup_active_v1(token, channel_id) == False: 
        raise InputError 
        queue = []
        for channel in get_data()['channels']:
            if channel['channel_id'] == channel_id:
                if channel['standup']['standup_active'] == True: 
                    standup_message_queue(token, message, channel_id)
    return {}


#### scrap code ### 

 
##helper function for storing the messages that aren't the last one## 

def standup_message_queue(token, message, channel_id):
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    for user in get_data()['users']: 
        if user['u_id'] = auth_user_id: 
            newuser = user['handle_str'] 
    standup_mess = newuser + ":" + message + '\n'
    for channel in get_data()['channels']: 
        if channel['channel_id'] == channel_id: 
            channel['standup']['message'] = channel['standup']['message'] + message

##pause and then after it's done grab the messages from standup_messages and send them 
def thread_helper(length, token, channel_id):
    time.sleep(length)
    auth_user_id = decode_token(token)
    channel['standup']['standup_active'] = False
    s_message = channel['standup']['standup_message']
    message_send_v1(token, channel_id, s_message)