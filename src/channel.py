from src.data_store import data_store, initial_object 
from src.error import InputError, AccessError
from src.channels import channels_create_check_valid_user, user_info

def channel_invite_v1(auth_user_id, channel_id, u_id):

    '''
    Invites a user with ID u_id to join a channel with ID channel_id. 
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users.
    '''
    store = data_store.get()

    # Invalid auth_user_id
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")
    if not isinstance(auth_user_id, int):
        raise AccessError("This is an invalid auth_user_id")

    # Invalid u_id
    if channels_create_check_valid_user(u_id) == False:
        raise AccessError("The u_id does not refer to a valid user")
    if not isinstance(u_id, int):
        raise AccessError("This is an invalid u_id")    

    # Input error when channel_id does not refer to a valid channel
    if check_channel_id(channel_id) == False:
        raise InputError("Channel_id does not refer to a valid channel")
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")

    # Input error when u_id refers to a user who is already a member of the channel
    if check_valid_member_in_channel(channel_id, u_id) == True:
        raise InputError("u_id is already a member of the channel")

    # Access error channel_id is valid and the authorised user is not a member of the channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("The authorised user is not a member of the channel")
    
    new_user = user_info(u_id)
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            # append the new user details to all_member
            channel['all_members'].append(new_user)

    data_store.set(store)
    return {}


def channel_details_v1(auth_user_id, channel_id):

    # Invalid auth_user_id
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth user id')

    # Invalid channel_id
    if check_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")

    # Inavlid auth_user_id
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")

    # Authorised user not a member of channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    channel_info = check_channel_id(channel_id)

    return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members'],
    }


def channel_messages_v1(auth_user_id, channel_id, start):
    
    # Invalid auth_user_id
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth user id')

    # Invalid channel_id
    if check_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")

    # Channel_id is valid and the authorised user is not a member of the channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    messages = []
    num_messages = len(messages)

    # Start is greater than the total number of messages in the channel
    if check_start_lt_total_messages(num_messages, start) == False:
        raise InputError("Index 'start' is greater than the total number of messages in channel")

    end = start + 50
    if end >= num_messages:
        end = -1
    

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

# Checks if the start is greater than total number of messages
def check_start_lt_total_messages(num_messages, start):
    if start > num_messages:
        return False
    else:
        return True


def channel_join_v1(auth_user_id, channel_id):
    '''
    raise error :
    input  
    - channel id not valid/doesn't have a valid channel 
    - authoried user is alreadt a member of the channel 
    access
    - when a channel is private and authorised user is not a member - also not global owner 

    to do: 
    take in an auth_user_id and channel id and append them to the member list in channels dictionary 
    ''' 
    store = data_store.get()
    
    # Invalid auth_user_id
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth user id')

    # Invalid channel_id
    if check_channel_id(channel_id) == False: 
        raise InputError('Channel id is not valid')
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")

    if check_valid_member_in_channel(channel_id, auth_user_id) == True:
        raise InputError ('Already a member of this channel')

    elif check_valid_member_in_channel (channel_id, auth_user_id) == False: 
        if check_channel_private(channel_id) == True: 
            raise AccessError ('Not authorised to join channel')

    new_user = user_info(auth_user_id)

    for channels in initial_object['channels']: 
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(new_user)

    data_store.set(store)
    return {
    }

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
