from src.data_store import data_store, initial_object 
from src.error import InputError, AccessError
from src.helper import check_valid_start, get_channel_details, check_valid_channel_id, user_info
from src.helper import check_valid_member_in_channel, check_channel_private, check_permision_id
from src.helper import channels_create_check_valid_user



def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id. 
    Once invited, the user is added to the channel immediately. 
    In both public and private channels, all members are able to invite users.

    Arguments:
        <auth_user_id> (<int>)    - unique id of an authorised user who is doing the inviting
        <channel_id>   (<int>)    - unique id if a channel
        <u_id>         (<int>)    - unique id of an authorised user who is being invited

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is already a member of the channel
                    
        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - Occurs when channel_id is valid and the authorised user is not a 
                      member of the channel

    Return Value:
        N/A
    '''

    store = data_store.get()

    # Invalid auth_user_id
    if not isinstance(auth_user_id, int) or channels_create_check_valid_user(auth_user_id) == False:
        # Invalid auth_user_id and invalid channel_id
        if check_valid_channel_id(channel_id) == False:
            raise AccessError("The auth_user_id and channel_id do not refer to a valid auth_user_id or channel_id")
        # Invalid auth_user_id and invalid u_id
        elif channels_create_check_valid_user(u_id) == False:
            raise AccessError("The auth_user_id and u_id do not refer to a valid auth_user_id or u_id")  
        # Invalid auth_user_id and u_id is already a member of the channel
        elif check_valid_member_in_channel(channel_id, u_id) == True:
            raise AccessError("The auth_user_id is invalid and the user with u_id is already a member of the channel")  
        else:
            raise AccessError("The auth_user_id does not refer to a valid user")

    # Invalid u_id
    if not isinstance(u_id, int) or channels_create_check_valid_user(u_id) == False: 
        # Access error channel_id is valid and authorised user is not a member of the channel
        # and the u_id is invalid
        if check_valid_member_in_channel(channel_id, auth_user_id) == False:
            raise AccessError("Authorised user is not a member of the channel and the u_id is invalid ")
        else:
            raise InputError("The u_id does not refer to a valid user")    

    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or check_valid_channel_id(channel_id) == False:
        raise InputError("Channel_id does not refer to a valid channel")

    # Input error when u_id refers to a user who is already a member of the channel
    if check_valid_member_in_channel(channel_id, u_id) == True:
        # Access error channel_id is valid and authorised user is not a member of the channel
        # and the u_id is already a member of the channel
        if check_valid_member_in_channel(channel_id, auth_user_id) == False:
            raise AccessError("The authorised user is not a member of the channel")
        else:
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
    '''
    Given a channel with ID channel_id that the authorised user 
    is a member of, provide basic details about the channel.

    Arguments:
        <auth_user_id> (<int>)    - unique id of an authorised user
        <channel_id>   (<int>)    - unique id if a channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - Occurs when channel_id is valid and the authorised user is not a member
                      of the channel

    Return Value:
        Returns <name> of valid channel requested by authorised user
        Returns <is_public> of valid channel requested by authorised user
        Returns <owner_members> of valid channel requested by authorised user
        Returns <all_members> of valid channel requested by authorised user
    '''

    # Invalid auth_user_id
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth_user_id')
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")
    
    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if check_valid_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")
   

    # Authorised user not a member of channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    channel_info = get_channel_details(channel_id)

    return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members'],
    }


def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    return up to 50 messages between index "start" and "start + 50". 

    Arguments:
        <auth_user_id> (<int>)    - unique id of an authorised user
        <channel_id>   (<int>)    - unique id of a channel
        <start>        (<int>)    - starting index of message pagination

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when start is greater than the total number of messages in the channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - Occurs when channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        Returns <messages> of valid channel requested by authorised user with valid starting index
        Returns <start> of valid channel requested by authorised user with valid starting index
        Returns <end> of valid channel requested by authorised user with valid starting index, 
            -1 if function has returned the least recent messages in the channel
    '''
    
    # Invalid auth_user_id
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth user id')
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")

    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if check_valid_channel_id(channel_id) == False:
        raise InputError("The channel_id does not refer to a valid channel")

    # Channel_id is valid and the authorised user is not a member of the channel
    if check_valid_member_in_channel(channel_id, auth_user_id) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    messages = []
    num_messages = len(messages)

    # Start is greater than the total number of messages in the channel
    if check_valid_start(num_messages, start) == False:
        raise InputError("Index 'start' is greater than the total number of messages in channel")

    end = start + 50
    if end >= num_messages:
        end = -1
    

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }


def channel_join_v1(auth_user_id, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join, 
    adds them to that channel.

    Arguments:
        <auth_user_id> (<int>)    - unique id of an authorised user
        <channel_id>   (<int>)    - unique id of a channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when the authorised user is already a member of the channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - channel_id refers to a channel that is private and the authorised 
                      user is not already a channel member and is not a global owner

    Return Value:
        N/A
    ''' 
    store = data_store.get()
    
    # Invalid auth_user_id
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth user id')
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError("The auth_user_id does not refer to a valid user")
    
    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if check_valid_channel_id(channel_id) == False: 
        raise InputError('Channel id is not valid')

    if check_valid_member_in_channel(channel_id, auth_user_id) == True:
        raise InputError ('Already a member of this channel')

    elif check_valid_member_in_channel (channel_id, auth_user_id) == False: 
        if check_channel_private(channel_id) == True and check_permision_id(auth_user_id) == False: 
            raise AccessError ('Not authorised to join channel')

    new_user = user_info(auth_user_id)

    for channels in initial_object['channels']: 
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(new_user)

    data_store.set(store)
    return {
    }

