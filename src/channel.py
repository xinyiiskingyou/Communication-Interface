from src.data_store import data_store, initial_object 
from src.error import InputError, AccessError
from src.channels import channels_create_check_valid_user, channels_user_details



def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    # Inavlid channel_id
    if details_check_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    channel_info = details_check_channel_id(channel_id)
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
    '''
    raise error :
    input  
    - channel id not valid/doesn't have a valid channel 
    - authoried user is alreadt a member of the channel 
    access
    - when a channel is private and authorised user is not a member - also not global owner 

    to do: 
    take in an authuserid and channel id and append them to the member list in channels dictionary 
    ''' 
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError ('Auth_user_id is not a valid id')
    if check_check_channel_id(channel_id) == False: 
        raise InputError('Channel id is not valid')
    if check_valid_member_in_channel(channel_id, auth_user_id) == True:
        raise InputError ('Already a member of this channel')
    elif check_valid_member_in_channel (channel_id, auth_user_id) == False: 
        if check_channel_private(channel_id) == True: 
            raise AccessError ('Not authorised to join channel')
    new_user = channels_user_details(auth_user_id)
    for channels in initial_object['channels']: 
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(new_user)
    return {
    }

# Helper function for channel_details
# Checks if a valid channel_id is being passed in or not
def details_check_channel_id(channel_id):
    store = data_store.get()
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    return False


def check_valid_member_in_channel(channel_id, auth_user_id):

    # for all channels
    # if the user has channel_id
    # if the users are authorised
    # return True
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            for member in channels['all_members']:
                if member['auth_user_id'] == auth_user_id:
                    return True
    
    return False

def check_channel_private(channel_id): 
    store = data_store.get()
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id: 
            if channels['is_public'] == False: 
                return True
            else: 
                return False
