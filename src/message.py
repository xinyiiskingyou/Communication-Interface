'''
Messages implementation
'''

from src.data_store import DATASTORE, initial_object
from src.error import InputError, AccessError
from src.helper import check_valid_channel_id, check_valid_member_in_channel, get_message_dict, check_valid_message
from src.helper import check_valid_message_id, check_authorised_user_edit, check_valid_message_send_format
from src.server_helper import decode_token, valid_user
import time

def message_send_v1(token, channel_id, message):
    '''
    Send a message from the authorised user to the channel specified by channel_id

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)      - unique id of a channel
        <message>      (<string>)   - the content of the message

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when length of message is less than 1 or over 1000 characters

        AccessError - Occurs when the channel_id is valid and the authorised user is 
                    not a member of the channel
                    - Occurs when token is invalid
    Return Value:
        Returns <message_id> of a valid message
    '''
    store = DATASTORE.get()
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

    # Creating unique message_id 
    message_id = (len(initial_object['messages']) * 2) + 1

    # Current time message was created and sent
    time_created = int(time.time())

    message_details_channels = {
        'message_id': message_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created
    }

    # Append dictionary of message details into initial_objects['channels']['messages']
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].insert(0, message_details_channels)

    message_details_messages = {
        'message_id': message_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created,
        'channel_id': channel_id
    }

    # Append dictionary of message details into intital_objects['messages']
    initial_object['messages'].insert(0, message_details_messages)

    DATASTORE.set(store)

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
        InputError  - Occurs when length of message is over 1000 characters
                    - Occurs when message_id does not refer to a valid message within a channel/DM 
                    that the authorised user has joined

        AccessError - Occurs when message_id refers to a valid message in a joined channel/DM 
                    and none of the following are true:
                        -  the message was sent by the authorised user making this request
                        -  the authorised user has owner permissions in the channel/DM
                    - Occurs when token is invalid
    Return Value:
        N/A
    '''
    store = DATASTORE.get()
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

    if message == '':
        messages = initial_object['messages']
        message_dict_remove = get_message_dict(message_id)
        messages.remove(message_dict_remove)

    for channel in initial_object['channels']:
        for iterate_message in channel['messages']:
            if iterate_message['message_id'] == message_id:
                if message == '':
                    channel['messages'].remove(iterate_message)
                else:
                    iterate_message['message'] = message


    for dm in initial_object['dms']:
        for iterate_message in dm['messages']:
            if iterate_message['message_id'] == message_id:
                if message == '':
                    dm['messages'].remove(iterate_message)
                else:
                    iterate_message['message'] = message
    
    DATASTORE.set(store)
    return {}
    
def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel/DM

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <message_id>   (<int>)      - unique id of a message

    Exceptions:
        InputError  - Occurs when message_id does not refer to a valid message within 
                    a channel/DM that the authorised user has joined

        AccessError - Occurs when message_id refers to a valid message in a joined channel/DM 
                    and none of the following are true:
                        -  the message was sent by the authorised user making this request
                        -  the authorised user has owner permissions in the channel/DM
                    - Occurs when token is invalid
    Return Value:
        N/A
    '''
    store = DATASTORE.get()
    
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    
    auth_user_id = decode_token(token)

    # Checks if message_id does not refer to a valid message within a channel/DM 
    # that the authorised user has joined
    if not check_valid_message_id(auth_user_id, message_id):
        raise InputError(description="The message_id is invalid.")
    
    # Checks if the message was sent by the authorised user making this request
    # AND/OR
    # the authorised user has owner permissions in the channel/DM
    if not check_authorised_user_edit(auth_user_id, message_id):
        raise AccessError(description="The user is unauthorised to edit the message.")

    # Given a message_id for a message, remove message from the channel/DM
    for channel in initial_object['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                channel['messages'].remove(message)

    for dm in initial_object['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                dm['messages'].remove(message)

    DATASTORE.set(store)

    return {}
