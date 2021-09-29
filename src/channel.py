from src.data_store import data_store, initial_object 
from src.error import InputError, AccessError
from src.channels import channels_create_check_valid_user, channels_user_details, channels_create_v1



def channel_invite_v1(auth_user_id, channel_id, u_id):

    '''
    Invites a user with ID u_id to join a channel with ID channel_id. 
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users.

    '''

    # Input error
    if check_channel_id(channel_id) == False:
        raise InputError("Channel_id does not refer to a valid channel")
    
    # how do you check valid u_id
    if check_valid_u_id(u_id) == False:
        raise InputError("u_id does not refer to a valid user")
    
    # Access error channel_id is valid and the authorised user is not a member of the channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("The authorised user is not a member of the channel")
    
    channels = initial_object['channels']
    new_user = channels_user_details(u_id)
    for channel in channels:
        if channel['channel_id'] == channel_id:
            # append the new user details to all_member
            channel['all_members'].append(new_user)
            
    return {}


def channel_details_v1(auth_user_id, channel_id):
   # Inavlid channel_id
    if check_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    channels = initial_object['channels']
    channel_info = check_channel_id(channel_id)
    return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': [
            {
                channels['owner_members'],
            }
        ],
        'all_members': [
            {
                channels['all_members'],
            }
        ],
    }

    '''return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members'],
    }'''


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
    if check_channel_id(channel_id) == False: 
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

# A helper function to check for valid u_id
def check_valid_u_id(u_id):
    # negative u_id
    if int(u_id) < 0:
        return False
    return True

# Checks if a valid channel_id is being passed in or not
def check_channel_id(channel_id):
    for channel in initial_object['channels']:
        if int(channel['channel_id']) == int(channel_id):
            return channel
    return False


def check_valid_member_in_channel(channel_id, auth_user_id):
    for channel in initial_object['channels']:
        if int(channel['channel_id']) == int(channel_id):
            for member in channel['all_members']:
                if int(member['auth_user_id']) == int(auth_user_id):
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
