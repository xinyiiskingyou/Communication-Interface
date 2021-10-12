'''
Channel implementation
'''
from src.error import InputError, AccessError
from src.helper import check_valid_start, get_channel_details, check_valid_channel_id, user_info
from src.helper import check_valid_member_in_channel, check_channel_private, check_permision_id
from src.helper import channels_create_check_valid_user, check_valid_owner, check_only_owner, check_global_owner
from src.data_store import DATASTORE, initial_object
from src.server_helper import decode_token

def channel_invite_v2(token, channel_id, u_id):

    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.

    Arguments:
        <token>        (<hash>)   - unique id of an authorised user who is doing the inviting
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
    auth_user_id = decode_token(token)
    store = DATASTORE.get()

    # Invalid u_id
    if not isinstance(u_id, int) or not channels_create_check_valid_user(u_id):
        # Access error channel_id is valid and authorised user is not a member of the channel
        # and the u_id is invalid
        if not check_valid_member_in_channel(channel_id, auth_user_id):
            raise AccessError("Authorised user is not a member of channel and u_id is invalid")
        raise InputError("The u_id does not refer to a valid user")

    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or not check_valid_channel_id(channel_id):
        raise InputError("Channel_id does not refer to a valid channel")

    # Input error when u_id refers to a user who is already a member of the channel
    if check_valid_member_in_channel(channel_id, u_id):
        # Access error channel_id is valid and authorised user is not a member of the channel
        # and the u_id is already a member of the channel
        if not check_valid_member_in_channel(channel_id, auth_user_id):
            raise AccessError("The authorised user is not a member of the channel")
        raise InputError("u_id is already a member of the channel")

    # Access error channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError("The authorised user is not a member of the channel")

    new_user = user_info(u_id)
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            # append the new user details to all_member
            channel['all_members'].append(new_user)

    DATASTORE.set(store)
    return {}

def channel_details_v2(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user
    is a member of, provide basic details about the channel.

    Arguments:
        <token>        (<hash>)   - an authorisation hash
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
    auth_user_id = decode_token(token)

    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if not check_valid_channel_id(channel_id):
        raise InputError("The channel_id does not refer to a valid channel")

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    channel_info = get_channel_details(channel_id)
    return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members'],
    }

def channel_messages_v2(token, channel_id, start):

    '''
    Given a channel with ID channel_id that the authorised user is a member of,
    return up to 50 messages between index "start" and "start + 50".

    Arguments:
        <token>        (<hash>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id of a channel
        <start>        (<int>)    - starting index of message pagination

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when start is greater than the total number of messages in the channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - Occurs when channel_id is valid and the authorised user is not a
                        member of the channel

    Return Value:
        Returns <messages> of valid channel requested by authorised user with valid starting index
        Returns <start> of valid channel requested by authorised user with valid starting index
        Returns <end> of valid channel requested by authorised user with valid starting index,
            -1 if function has returned the least recent messages in the channel
    '''

    auth_user_id = decode_token(token)
    
    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if not check_valid_channel_id(channel_id):
        raise InputError("The channel_id does not refer to a valid channel")

    # Channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    messages = []
    num_messages = len(messages)

    # Start is greater than the total number of messages in the channel
    if not check_valid_start(num_messages, start):
        raise InputError("Index 'start' is greater than the total number of messages in channel")

    end = start + 50
    if end >= num_messages:
        end = -1

    return {
        'messages': messages,
        'start': start,
        'end': end,
    }

def channel_join_v2(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel.

    Arguments:
        <token>        (<hash>)   - an authorisation hash
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
    store = DATASTORE.get()
    auth_user_id = decode_token(token)

    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if not check_valid_channel_id(channel_id):
        raise InputError('Channel id is not valid')

    if check_valid_member_in_channel(channel_id, auth_user_id):
        raise InputError('Already a member of this channel')

    if not check_valid_member_in_channel (channel_id, auth_user_id):
        if check_channel_private(channel_id) and not check_permision_id(auth_user_id):
            raise AccessError ('Not authorised to join channel')

    new_user = user_info(auth_user_id)

    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            channels['all_members'].append(new_user)

    DATASTORE.set(store)
    return {}

def channel_addowner_v1(token, channel_id, u_id):
    '''
    Make user with user id u_id an owner of the channel

    Arguments:
        <token>        (<hash>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id of a channel
        <u_id>         (<int>)    - an unique auth_user_id of the user to
                                    be added as an owner of the channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is not a member of the channel

        AccessError - Occurs when channel_id is valid and the auth user doesn't have owner
                      permission in the channel

    Return Value:
        N/A
    '''
    store = DATASTORE.get()
    auth_user_id = decode_token(token)
    print(check_valid_member_in_channel(channel_id, auth_user_id))
    #print(isinstance(channel_id, int))
    # invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError("This is an invalid channel_id")
    if not check_valid_channel_id(channel_id):
        raise InputError('Channel id is not valid')

    # invalid u_id
    if not isinstance(u_id, int):
        raise InputError("This is an invalid u_id")
    if not channels_create_check_valid_user(u_id):
        raise InputError("user is not valid")

    # u_id not a member of the channel
    if not check_valid_member_in_channel(channel_id, u_id):
        raise InputError("User is not a member of the channel")
    
    # u_id already owner of the channel
    if check_valid_owner(u_id, channel_id):
        raise InputError("User is already an owner of the channel")

    # No owner permission
    if not check_valid_owner(auth_user_id, channel_id):
        if not check_global_owner(auth_user_id):
            raise AccessError("Doesn't have owner permission in the channel") 
    user = user_info(u_id)
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            channels['owner_members'].append(user)

    DATASTORE.set(store)
    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    Remove user with user id u_id as an owner of the channel.

    Arguments:
        <token>        (<hash>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id of a channel
        <u_id>         (<int>)    - an unique auth_user_id of the user to
                                    be removed as an owner of the channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is not an owner of the channel
                    - Occurs when u_id refers to a user who is currently the only owner of the channel

        AccessError - Occurs when channel_id is valid and the auth user doesn't have owner
                    permission in the channel

    Return Value:
        N/A
    '''
    auth_user_id = decode_token(token)

    store = DATASTORE.get()
    # channel_id does not refer to a valid channel
    if not check_valid_channel_id(channel_id) or not isinstance(channel_id, int):
        raise InputError("The channel_id does not refer to a valid channel")

    # u_id does not refer to a valid user
    if not channels_create_check_valid_user(u_id) or not isinstance(u_id, int):
        raise InputError("The u_id does not refer to a valid user")
    
    # u_id refers to a user who is not an owner of the channel
    if not check_valid_owner(u_id, channel_id):
        raise InputError("The u_id does not refer to a user who is not an owner of the channel")

    # u_id refers to a user who is currently the only owner of the channel
    channel = check_only_owner(u_id, channel_id)
    if len(channel['owner_members']) == 1:
        raise InputError("The u_id refers to a user who is currently the only owner of the channel")
    
    # channel_id is valid and the authorised user does not have owner permissions in the channel
    if not check_valid_owner(auth_user_id, channel_id):
        for user in initial_object['users']:
            if user['permission_id'] != 1:
                raise AccessError("The authorised user does not have owner permissions in the channel")

    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            for owner in channel['owner_members']:
                if owner['u_id'] == u_id:
                    channel['owner_members'].remove(owner)

    DATASTORE.set(store)
    return {}
