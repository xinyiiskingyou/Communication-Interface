'''
Messages implementation
'''

from src.data_store import DATASTORE, initial_object
from src.error import InputError, AccessError
from src.helper import check_valid_channel_id, check_valid_member_in_channel
from src.server_helper import decode_token

def message_send_v1(token, channel_id, message):
    
    auth_user_id = decode_token(token)
    store = DATASTORE.get()

    # Invalid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError("The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    