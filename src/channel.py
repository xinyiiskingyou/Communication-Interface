from src.data_store import data_store, initial_object
from src.error import InputError, AccessError

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # Inavlid channel_id
    if check_valid_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    channel_info = check_valid_channel_id(channel_id)
    return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members'],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }

# Helper function for channel_details
# Checks if a valid channel_id is being passed in or not
def check_valid_channel_id(channel_id):
    store = data_store.get()
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return False

# Check if user with valid channel_id is not a member of the channel
def check_valid_member_in_channel(channel_id, auth_user_id):
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['auth_user_id'] == auth_user_id:
                    return True
    return False

