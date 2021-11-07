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
            # channel['standup']['u_id_start'] = auth_user_id
            t1 = threading.Thread(target = standup_send_v1, args=[token, channel_id, message])
            # t2 = threading.Thread(target = thread_helper, args = [token, channel_id, message])
            channel['standup']['standup_active'] = True
            t1.start()
            time.sleep(length)
            t1.end()
            channel['standup']['standup_active'] = False
            channel['standup']['time_finished'] = time_finish
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
            if : 
                standup_message_queue(token, message, queue)
            else: 
                standup_message = queue_compile(queue, message)
                channel['standup']['standup_message'] = standup_message
                ####figure out how to actually sned the message (like message send) 
                get_data()['messages'].insert(0, message_details_messages)
                save()
    return {}


#### scrap code ### a

    # t1 = threading.Thread(target=standup_start_v1)
# t2 = threading.Thread(target=standup_start_v1)
    #     print(f'starting for {length}')
#     bool time_finish = False
#     time.sleep(length)
#     print("end of standup")
#     time_finish = True
#     return time_finish 

##while the standup start is paused - process all the messages and queue in send? 
# def thread_helper(length, message):
#     start_time = time.time() 

#     while True: 
#         currtime = time.tine()
#         time_past = currtime - start_time

#         if (currtime > length): 
#             break
    ##message id
    # message_id = (len(get_data()['messages']) * 2) + 1
    #  # Append dictionary of message details into initial_objects['channels']['messages']
    #  ##get the channel ... tho it i should change the helper function parameters for this 
    #  ##and then append it the message to a list????? 
    #  queue = []
    # for channel in get_data()['channels']:
    #     if channel['channel_id'] == channel_id:
    #         channel['messages'].insert(0, message_details_channels)
    #         save()

    # message_details_messages = {
    #     'message_id': message_id,
    #     'u_id': auth_user_id, 
    #     'message': message,
    #     'time_created': time_created,
    #     'channel_id': channel_id,
    #     'reacts':[reacts_details],
    #     'is_pinned': bool(is_pinned)
    # }


##might help with the last bit of creation
# def message_create_for_standup(channel_id, u_id, message):
#     user = u_id_check(u_id)
#     channel = channel_check(channel_id)
#     final_string = channel["standup"]["standup_message"]
#     return_string = user['handle_str'] + ":" + message + '\n'
#     channel["standup"]["standup_message"] = final_string + return_string


##so basically thread to standup send - append each message and then when the time runs out 
##compile and 


##helper function for storing the messages that aren't the last one## 

def standup_message_queue(token, message, queue):
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    for user in get_data()['users']: 
        if user['u_id'] = auth_user_id: 
            newuser = user['handle_str'] 
    standup_mess = newuser + ":" + message + '\n'
    queue.append(standup_mess)

def queue_compile(queue, message): 
    for user in get_data()['users']: 
        if user['u_id'] = auth_user_id: 
            newuser = user['handle_str']
    new_message =  newuser + ":" + message + '\n'
    for x in queue:
        new_message = new_message + x
    return new_message
        
# not channel['standup']['time_finished'] - datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() > 0