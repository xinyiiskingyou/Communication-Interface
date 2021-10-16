'''
Messages implementation
'''

from src.data_store import DATASTORE, initial_object
from src.error import InputError, AccessError
from src.helper import check_valid_channel_id, check_valid_member_in_channel, check_valid_message
from src.server_helper import decode_token
import time

def message_send_v1(token, channel_id, message):
    
    auth_user_id = decode_token(token)
    store = DATASTORE.get()

    # Invalid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError("The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    # Invalid message: Less than 1 or over 1000 characters
    if not check_valid_message(message):
        raise InputError("Message is invalid as length of message is less than 1 or over 1000 characters.")

    # Creating unique message_id 
    message_id = (len(initial_object['messages']) * 2) + 1

    # Current time message was created and sent
    time_created = time.time()

    message_details = {
        'message_id': message_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created
    }

    # Append dictionary of message details into initial_objects['channels']['messages']
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(message_details)

    # Append dictionary of message details into intital_objects['messages']
    message_details['channel_id'] = channel_id
    initial_object['messages'].append(message_details)

    DATASTORE.set(store)

    return {
        'message_id': message_id
    }