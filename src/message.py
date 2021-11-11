'''
Messages implementation
'''
import time
from src.data_store import get_data, save
from src.error import InputError, AccessError
from src.helper import check_valid_channel_id, check_valid_member_in_channel, check_valid_message
from src.helper import check_authorised_user_edit, check_valid_message_send_format, check_authorised_user_pin
from src.helper import get_message, check_valid_channel_dm_message_ids, get_channel_details
from src.helper import check_valid_dm, check_valid_member_in_dm, get_reacts, check_valid_message_id
from src.helper import check_valid_channel_id_and_dm_id_format, check_share_message_authorised_user
from src.helper import check_message_channel_tag, user_stats_update_messages, get_dm_dict
from src.helper import users_stats_update_messages, new_react, get_msg_details, get_msg_details_channels
from src.helper import get_msg_details_dm
from src.server_helper import decode_token, valid_user
from src.notifications import activate_notification_tag_channel, activate_notification_react
from src.dm import message_senddm_v1

def message_send_v1(token, channel_id, message):
    '''
    Send a message from the authorised user to the channel specified by channel_id

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)      - unique id of a channel
        <message>      (<string>)   - the content of the message

    Exceptions:
        InputError      - Occurs when channel_id does not refer to a valid channel
                        - Occurs when length of message is less than 1 or over 1000 characters

        AccessError     - Occurs when the channel_id is valid and the authorised user is 
                        not a member of the channel
                        - Occurs when token is invalid
    Return Value:
        Returns <message_id> of a valid message
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    
    # Invalid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description="The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description="Authorised user is not a member of channel with channel_id")

    # Invalid message: Less than 1 or over 1000 characters
    if not check_valid_message(message):
        raise InputError(description="Message is invalid as length of message is less than 1 or over 1000 characters.")

    # Checks if message contains a tag to an authorised user
    tagged_user_list = check_message_channel_tag(message, channel_id)
    if tagged_user_list != []:
        activate_notification_tag_channel(auth_user_id, tagged_user_list, channel_id, message)
    
    # Creating unique message_id 
    message_id = (len(get_data()['messages']) * 2) + 1
    # Current time message was created and sent
    time_created = int(time.time())

    is_this_user_reacted = False
    is_pinned = False
    reacts_details = new_react(is_this_user_reacted)

    msg_details_channels = get_msg_details(message_id, auth_user_id, message, 
                                            time_created, reacts_details, is_pinned)
    # Append dictionary of message details into initial_objects['channels']['messages']
    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].insert(0, msg_details_channels)
            save()
    
    msg_details_msgs = get_msg_details_channels(message_id, auth_user_id, message,time_created,
                                                        channel_id, reacts_details, is_pinned)

    # Append dictionary of message details into intital_objects['messages']
    get_data()['messages'].insert(0, msg_details_msgs)
    save()

    # For user/stats, append a new stat in 'messages_sent'
    user_stats_update_messages(auth_user_id, 1)
    save()

    # For users/stats, append new stat in 'messages_exist'
    users_stats_update_messages(1)
    save()

    return {
        'message_id': message_id
    }

def message_edit_v1(token, message_id, message):
    '''
    Given a message, update its text with new text. 

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message
        <message>      (<string>)   - the new content of the message

    Exceptions:
        InputError      - Occurs when length of message is over 1000 characters
                        - Occurs when message_id does not refer to a valid message within a channel/DM 
                        that the authorised user has joined

        AccessError     - Occurs when message_id refers to a valid message in a joined channel/DM 
                        and none of the following are true:
                        - The message was sent by the authorised user making this request
                        - The authorised user has owner permissions in the channel/DM
                        - Occurs when token is invalid
    Return Value:
        N/A
    '''

    auth_user_id = decode_token(token)
    
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    # Input and Access Error are raised -> Access Error
    # Invalid message AND (checks if message was sent by auth user making request AND/OR 
    # the authorised user has owner permissions in the channel/DM)
    if not check_valid_message_send_format(message) and not check_authorised_user_edit(auth_user_id, message_id):
        raise AccessError(description="The user is unauthorised to edit the message.")

    # Invalid message: Less than 1 or over 1000 characters
    if not check_valid_message_send_format(message):
        raise InputError(description="Message is invalid as length of message is less than 1 or over 1000 characters.")

    # Checks if message_id does not refer to a valid message within a channel/DM 
    # that the authorised user has joined
    if not check_valid_message_id(auth_user_id, message_id):
        raise InputError(description="The message_id is invalid.")

    # Checks if the message was sent by the authorised user making this request
    # AND/OR
    # the authorised user has owner permissions in the channel/DM
    if not check_authorised_user_edit(auth_user_id, message_id):
        raise AccessError(description="The user is unauthorised to edit the message.")
    
    for channel in get_data()['channels']:
        for iterate_message in channel['messages']:
            if iterate_message['message_id'] == message_id:
                if message == '':
                    channel['messages'].remove(iterate_message)
                else:
                    iterate_message['message'] = message
            save()

    for dm in get_data()['dms']:
        for iterate_message in dm['messages']:
            if iterate_message['message_id'] == message_id:
                if message == '':
                    dm['messages'].remove(iterate_message)
                else:
                    iterate_message['message'] = message
            save()
            
    if message == '':
        # For users/stats, append new stat in 'messages_exist'
        users_stats_update_messages(1)
        save()
        # For user/stat, append new stat in 'messages_sent'
        user_stats_update_messages(auth_user_id, -1)
        save()

    return {}
    
def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message

    Exceptions:
        InputError      - Occurs when message_id does not refer to a valid message within 
                        a channel/DM that the authorised user has joined

        AccessError     - Occurs when message_id refers to a valid message in a joined channel/DM 
                        and none of the following are true:
                        - The message was sent by the authorised user making this request
                        - The authorised user has owner permissions in the channel/DM
                        - Occurs when token is invalid
    Return Value:
        N/A
    '''
    
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)

    # Checks if message_id does not refer to a valid message within a channel/DM 
    # that the authorised user has joined
    if not check_valid_channel_dm_message_ids(message_id):
        raise InputError(description="The message_id is invalid.")
    
    # Checks if the message was sent by the authorised user making this request
    # AND/OR
    # the authorised user has owner permissions in the channel/DM
    if not check_authorised_user_edit(auth_user_id, message_id):
        raise AccessError(description="The user is unauthorised to edit the message.")

    # Given a message_id for a message, remove message from the channel/DM
    for channel in get_data()['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                channel['messages'].remove(message)
                save()
    
    for dm in get_data()['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                dm['messages'].remove(message)
                save()

    # For users/stats, append new stat in 'messages_exist'
    users_stats_update_messages(-1)
    save()
    # For user/stat, append new stat in 'messages_sent'
    user_stats_update_messages(auth_user_id, -1)
    save()
    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    Share an existing message to a channel/DM. An optional additional message in addition to the 
    shared message may be made. 

    Arguments:
        <token>           (<string>)   - an authorisation hash
        <og_message_id>   (<int>)      - unique id of a message
        <message>         (<string>)   - the content of the additional optional message
        <channel_id>      (<int>)      - unique id of a channel
        <dm_id>           (<int>)      - unique id of a DM

    Exceptions:
        InputError      - Occurs when both channel_id and dm_id are invalid
                        - Occurs when neither channel_id nor dm_id are -1
                        - Occurs when og_message_id does not refer to a valid message within a 
                        channel/DM that the authorised user has joined
                        - Occurs when length of message is more than 1000 characters

        AccessError     - Occurs when the pair of channel_id and dm_id are valid 
                        (i.e. one is -1, the other is valid) and the authorised user has not 
                        joined the channel or DM they are trying to share the message to
    Return Value:
        Returns <message_id> of the valid shared message
    '''

    # Checks for invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
        
    # Checks that the both channel_id and dm_id are valid
    if not check_valid_channel_id_and_dm_id_format(channel_id, dm_id):
        raise InputError(description="Both channel_id and dm_id are invalid.")

    # Given that pair of channel_id and dm_id are valid
    # checks that authorised user has joined the channel or DM they are trying to share the message to
    if not check_share_message_authorised_user(auth_user_id, channel_id, dm_id):
        raise AccessError(description="Authorised user has not joined channel or DM they are trying to share message to.")
    
    # Checks if og_message_id does not refer to a valid message within a channel/DM 
    # that the authorised user has joined
    if not check_valid_message_id(auth_user_id, og_message_id):
        raise InputError(description="The og_message_id is invalid.")

    # Checks that length of message is valid 
    if not check_valid_message_send_format(message):
        raise InputError(description="Length of message is more than 1000 characters.")

    og_message = get_message(og_message_id)['message']
    shared_message = f"'''\n{og_message}\n'''"
    
    if message != '':
        shared_message = f"{message}\n\n{shared_message}"

    if channel_id != -1:
        shared_message_id = message_send_v1(token, channel_id, shared_message)['message_id']
    if dm_id != -1:
        shared_message_id = message_senddm_v1(token, dm_id, shared_message)['message_id']

    return {
        'shared_message_id': shared_message_id
    }


def message_react_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of, 
    add a "react" to that particular message.

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message
        <react_id>     (<int>)      - the id of a react

    Exceptions:
        InputError      - Occurs when message_id is not a valid message within a channel or DM 
                        that the authorised user has joined
                        - Occurs when react_id is not a valid react ID
                        - Occurs when the message already contains a react with ID react_id from the authorised user

        AccessError     - Occurs when token is invalid
    
    Return Value:
        N/A
    '''
    
    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)
    react_id = int(react_id)
    message_id = int(message_id)

    # message_id is not valid
    if not check_valid_channel_dm_message_ids(message_id):
        raise InputError(description="The message_id is invalid.")

    # react id is not valid
    if react_id != 1:
        raise InputError(description="The react_id is invalid.")
    
    react = get_reacts(message_id, react_id)
    # the message already contains a react with ID react_id
    if auth_user_id in react['u_ids']:
        raise InputError(description= "Message already contains a react with ID react_id")

    react['u_ids'].append(int(auth_user_id))
    react['is_this_user_reacted'] = True
    save()

    # Activate notification for react
    activate_notification_react(auth_user_id, message_id)
    
    return {}
    
def message_unreact_v1(token, message_id, react_id):
    '''
    Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message.

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message
        <react_id>     (<int>)      - the id of a react

    Exceptions:
        InputError      - Occurs when message_id is not a valid message within a channel or DM 
                        that the authorised user has joined
                        - Occurs when react_id is not a valid react ID
                        - Occurs when the message does not contain a react with ID react_id from the authorised user

        AccessError     - Occurs when token is invalid
    
    Return Value:
        N/A
    '''

    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)
    react_id = int(react_id)
    message_id = int(message_id)

    # message_id is not valid
    if not check_valid_channel_dm_message_ids(message_id):
        raise InputError(description="The message_id is invalid.")

    # react id is not valid
    if react_id != 1:
        raise InputError(description="The react_id is invalid.")
    
    # the message does not contain a react with ID react_id
    react = get_reacts(message_id, react_id)
    if auth_user_id not in react['u_ids']:
        raise InputError(description= "Message already contains a react with ID react_id")

    react['u_ids'].remove(int(auth_user_id))
    react['is_this_user_reacted'] = False
    save()
    return {}

def message_pin_v1(token, message_id):
    '''
    Given a message within a channel or DM, mark it as "pinned".

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message

    Exceptions:
        InputError      - Occurs when message_id is not a valid message within a channel or DM 
                        that the authorised user has joined
                        - Occurs when the message is already pinned

        AccessError     - Occurs when token is invalid
                        - Occurs when message_id refers to a valid message in a joined channel/DM and 
                        the authorised user does not have owner permissions in the channel/DM
    
    Return Value:
        N/A
    '''

    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)
    message_id = int(message_id)

    # message_id refers to a valid message in a joined channel/DM and 
    # the authorised user does not have owner permissions in the channel/DM
    if not check_authorised_user_pin(message_id, auth_user_id):
        raise AccessError(description="The user is unauthorised to pin the message.")
    
    # message_id is not valid
    if not check_valid_channel_dm_message_ids(message_id):
        raise InputError(description="The message_id is invalid.")
    
    # message is already pinned
    message = get_message(message_id)
    if message['is_pinned'] == True:
        raise InputError(description="The message is already pinned.")

    message['is_pinned'] = True
    save()
    return {}

def message_unpin_v1(token, message_id):
    '''
    Given a message within a channel or DM, remove its mark as "pinned".

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message

    Exceptions:
        InputError      - Occurs when message_id is not a valid message within a channel or DM 
                          that the authorised user has joined
                        - Occurs when the message is not already pinned

        AccessError     - Occurs when token is invalid
                        - Occurs when message_id refers to a valid message in a joined channel/DM and 
                          the authorised user does not have owner permissions in the channel/DM
    
    Return Value:
        N/A
    '''

    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)
    message_id = int(message_id)

    # message_id is not valid
    if not check_valid_channel_dm_message_ids(message_id):
        raise InputError(description="The message_id is invalid.")
        
    # message_id refers to a valid message in a joined channel/DM and 
    # the authorised user does not have owner permissions in the channel/DM
    if not check_authorised_user_pin(message_id, auth_user_id):
        raise AccessError(description="The user is unauthorised to unpin the message.")
        
    # message is not already pinned
    message = get_message(message_id)
    if message['is_pinned'] == False:
        raise InputError(description="The message is not already pinned.")

    message['is_pinned'] = False
    save()
    return {}

def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Send a message from the auth_user to channel specified by channel_id
    automatically at a specified time in the future

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)      - unique id of a message
        <message>      (<string>)   - an authorisation hash
        <time_sent>    (<int>)      - time to send out the message

    Exceptions:
        InputError      - Occurs when channel_id is not valid
                        - Occurs when length of message is over 1000 characters
                        - Occurs when the time_sent is a time in the past

        AccessError     - Occurs when token is invalid
                        - Occurs when channel_id is valid and the auth_user is not a member of 
                          the channel they are trying to post to
    
    Return Value:
        <message_id>  (<int>)     - a valid message
    '''
    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)

    if not check_valid_channel_id(channel_id):
        raise InputError(description='Channel id does not refer to a valid channel')
    
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description='authorised user is not a member of the channel they are trying to post to')
    
    if len(message) > 1000:
        raise InputError(description='The length of message is over 1000 characters')
    
    if int(time.time()) > int(time_sent):
        raise InputError(description='Time_sent is a time in the past')

    # generate a message_id as soon as message_sendlater is called
    message_id = (len(get_data()['messages']) * 2) + 1

    # wait for [time_wait] amount of time
    time_wait = time_sent - int(time.time())
    time.sleep(time_wait)

    is_this_user_reacted = False
    is_pinned = False

    reacts_details = new_react(is_this_user_reacted)

    msg_details_channels = get_msg_details(message_id, auth_user_id, message, 
                                                time_sent, reacts_details, is_pinned)

    # Append dictionary of message details into initial_objects['channels']['messages']
    channel = get_channel_details(channel_id)
    channel['messages'].insert(0, msg_details_channels)
    save()

    msg_details_msgs = get_msg_details_channels(message_id, auth_user_id, message, time_sent, 
                                                        channel_id, reacts_details, is_pinned)

    # Append dictionary of message details into intital_objects['messages']
    get_data()['messages'].insert(0, msg_details_msgs)
    save()

    # For user/stats, append a new stat in 'messages_sent'
    user_stats_update_messages(auth_user_id, 1)
    save()

    # For users/stats, append new stat in 'messages_exist'
    users_stats_update_messages(1)
    save()

    return {
        'message_id': message_id
    }

def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Send a message from the auth_user to dm specified by dm_id
    automatically at a specified time in the future

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <dm_id>        (<int>)      - unique id of a message
        <message>      (<string>)   - an authorisation hash
        <time_sent>    (<int>)      - time to send out the message

    Exceptions:
        InputError      - Occurs when dm_id is not valid
                        - Occurs when length of message is over 1000 characters
                        - Occurs when the time_sent is a time in the past

        AccessError     - Occurs when token is invalid
                        - Occurs when dm_id is valid and the auth_user is not a member of 
                          the channel they are trying to post to
    
    Return Value:
        <message_id>  (<int>)     - a valid message
    '''
    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)

    if not check_valid_dm(dm_id):
        raise InputError(description='Dm id does not refer to a valid channel')
    
    if not check_valid_member_in_dm(dm_id, auth_user_id):
        raise AccessError(description='authorised user is not a member of the dm they are trying to post to')
    
    if len(message) > 1000:
        raise InputError(description='The length of message is over 1000 characters')
    
    if int(time.time()) > int(time_sent):
        raise InputError(description='Time_sent is a time in the past')

    # generate a message_id as soon as message_sendlater is called
    message_id = (len(get_data()['messages']) * 2)

    # wait for [time_wait] amount of time
    time_wait = time_sent - int(time.time())
    time.sleep(time_wait)

    is_this_user_reacted = False
    is_pinned = False

    reacts_details = new_react(is_this_user_reacted)

    msg_details_dm = get_msg_details(message_id, auth_user_id, message, 
                                        time_sent, reacts_details, is_pinned)

    # Append dictionary of message details into initial_objects['dms']['messages']
    dm = get_dm_dict(dm_id)
    dm['messages'].insert(0, msg_details_dm)
    save()

    msg_details_msgs = get_msg_details_dm(message_id, auth_user_id, message, time_sent, 
                                                    dm_id, reacts_details, is_pinned)

    # Append dictionary of message details into intital_objects['messages']
    get_data()['messages'].insert(0, msg_details_msgs)
    save()

    # For user/stats, append a new stat in 'messages_sent'
    user_stats_update_messages(auth_user_id, 1)
    save()

    # For users/stats, append new stat in 'messages_exist'
    users_stats_update_messages(1)
    save()

    return {
        'message_id': message_id
    }