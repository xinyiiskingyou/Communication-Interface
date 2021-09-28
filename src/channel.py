from src.channels import channels_user_details
from src.error import InputError, AccessError
from src.data_store import data_store, initial_object
from src.helper import check_valid_channel_id, check_valid_member_in_channel

def channel_invite_v1(auth_user_id, channel_id, u_id):

    '''
    Invites a user with ID u_id to join a channel with ID channel_id. 
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users.

    u_id refers to a user who is already a member of the channel
    '''

    # Input error
    if not check_valid_channel_id(channel_id):
        raise InputError("Channel_id does not refer to a valid channel")
    
    # how do you check valid u_id
    if not check_valid_u_id(u_id):
        raise InputError("u_id does not refer to a valid user")
    
    # Access error channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError("The authorised user is not a member of the channel")
    
    channels = initial_object['channels']
    new_user = channels_user_details(u_id)
    for channel in channels:
        if channel['channel_id'] == channel_id:
            # append the new user details to all_member
            channel['all_members'].append(new_user)

    return {}

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
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

# A helper function to check for valid u_id
def check_valid_u_id(u_id):
    
    # negative u_id
    if u_id <= 0:
        return False
    return True


