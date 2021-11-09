'''
Channel implementation
'''
import time
from src.error import InputError, AccessError
from src.helper import check_valid_start, get_channel_details, check_valid_channel_id, user_info
from src.helper import check_valid_member_in_channel, check_channel_private, check_permision_id, get_user_details, get_user_leave_channel_stats
from src.helper import channels_create_check_valid_user, check_valid_owner, check_channel_owner_permission, get_user_channel_stats
from src.notifications import activate_notification_channel_invite
from src.data_store import save, get_data
from src.server_helper import decode_token, valid_user

def channel_invite_v2(token, channel_id, u_id):

    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.

    Arguments:
        <token>        (<string>)   - unique id of an authorised user who is doing the inviting
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
                    - Occurs when token is invalid

    Return Value:
        N/A
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Input error when channel_id does not refer to a valid channel
    if not isinstance(channel_id, int) or not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel_id does not refer to a valid channel')

    # Access error channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'The authorised user is not a member of the channel')
    
    # Invalid u_id
    if not isinstance(u_id, int) or not channels_create_check_valid_user(u_id):
        raise InputError(description = 'The u_id does not refer to a valid user')

    # Input error when u_id refers to a user who is already a member of the channel
    if check_valid_member_in_channel(channel_id, u_id):
        raise InputError(description = 'u_id is already a member of the channel')

    new_user = user_info(u_id)
    get_user_channel_stats(auth_user_id)
    save()
    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            # append the new user details to all_member
            channel['all_members'].append(new_user)
            channel['time_stamp'] = int(time.time())
            save()
    # Activate notification for invite/add
    activate_notification_channel_invite(auth_user_id, channel_id, u_id)

    return {}

def channel_details_v2(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user
    is a member of, provide basic details about the channel.

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id if a channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - Occurs when channel_id is valid and the authorised user is not a member
                      of the channel
                    - Occurs when token is invalid

    Return Value:
        Returns <name> of valid channel requested by authorised user
        Returns <is_public> of valid channel requested by authorised user
        Returns <owner_members> of valid channel requested by authorised user
        Returns <all_members> of valid channel requested by authorised user
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Invalid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description = 'The channel_id does not refer to a valid channel')

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'Authorised user is not a member of channel with channel_id')

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
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id of a channel
        <start>        (<int>)    - starting index of message pagination

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when start is greater than the total number of messages in the channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - Occurs when channel_id is valid and the authorised user is not a
                        member of the channel
                    - Occurs when token is invalid

    Return Value:
        Returns <messages> of valid channel requested by authorised user with valid starting index
        Returns <start> of valid channel requested by authorised user with valid starting index
        Returns <end> of valid channel requested by authorised user with valid starting index,
            -1 if function has returned the least recent messages in the channel
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Invalid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description = 'The channel_id does not refer to a valid channel')

    # Channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'Authorised user is not a member of channel with channel_id')

    for channel in get_data()['channels']:
        if channel['channel_id'] == channel_id:
            num_messages = len(channel['messages'])
            message_pagination = channel['messages']
            save()
            
    # if this function has returned the least recent messages in the channel,
    # returns -1 in "end" to indicate there are no more messages to load after this return
    end = start + 50
    if end >= num_messages:
        end = -1

    # Start is greater than the total number of messages in the channel
    if not check_valid_start(num_messages, start):
        raise InputError(description = 'Index start is greater than the total number of messages in channel')

    # Pagination 
    if end == -1:
        message_pagination = message_pagination[start:]
    else:
        message_pagination = message_pagination[start:end]
        
    return {
        'messages': message_pagination,
        'start': start,
        'end': end,
    }

def channel_join_v2(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel.

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id of a channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when the authorised user is already a member of the channel

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user
                    - channel_id refers to a channel that is private and the authorised
                    user is not already a channel member and is not a global owner
                    - Occurs when token is invalid

    Return Value:
        N/A
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    
    # Invalid channel_id
    if not isinstance(channel_id, int):
        raise InputError(description = 'This is an invalid channel_id')
    if not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel id is not valid')

    # channel_id refers to a channel that is private and the 
    # authorised user is not already a channel member and is not a global owner
    if not check_valid_member_in_channel (channel_id, auth_user_id):
        if check_channel_private(channel_id) and not check_permision_id(auth_user_id):
            raise AccessError (description = 'Not authorised to join channel')

    # the authorised user is already a member of the channel
    if check_valid_member_in_channel(channel_id, auth_user_id):
        raise InputError(description = 'Already a member of this channel')

    get_user_channel_stats(auth_user_id)
    save()
    new_user = user_info(auth_user_id)
    channel = get_channel_details(channel_id)
    channel['all_members'].append(new_user)
    channel['time_stamp'] = int(time.time())
    save()
    return {}

def channel_leave_v1(token, channel_id):
    ''' 
    Given a channel with ID channel_id that the authorised user is a member of, 
    remove them as a member of the channel. Their messages should remain in the 
    channel. If the only channel owner leaves, the channel will remain.

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)      - unique id of a channel
    
    Exceptions:  
        InputError  - Occurs when channel_id does not refer to a valid channel 
        AccessError - Occurs when channel_id is valid but the auth user is not part of the channel 
                    - Occurs when token is invalid

     Return Value:
        N/A
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # channel_id does not refer to a valid channel
    if not isinstance(channel_id, int):
        raise InputError(description = 'This is an invalid channel_id')
    if not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel id is not valid')

    # channel_id is valid and the authorised user is not a member of the channel
    if not check_valid_member_in_channel(channel_id, auth_user_id):
        raise AccessError(description = 'The authorised user is not a member of the channel')

    get_user_leave_channel_stats(auth_user_id)
    save()
    channels = get_channel_details(channel_id)
    for member in channels['all_members']: 
        if member['u_id'] == auth_user_id:
            channels['all_members'].remove(member)
            member['is_removed'] = True
            save()
    for owner in channels['owner_members']: 
        if owner['u_id'] == auth_user_id:
            channels['owner_members'].remove(owner)
            owner['is_removed'] = True
            save()
    
    return {}

def channel_addowner_v1(token, channel_id, u_id):
    '''
    Make user with user id u_id an owner of the channel

    Arguments:
        <token>        (<string>)   - an authorisation hash
        <channel_id>   (<int>)    - unique id of a channel
        <u_id>         (<int>)    - an unique auth_user_id of the user to
                                    be added as an owner of the channel

    Exceptions:
        InputError  - Occurs when channel_id does not refer to a valid channel
                    - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is not a member of the channel

        AccessError - Occurs when channel_id is valid and the auth user doesn't have owner
                    permission in the channel
                    - Occurs when token is invalid

    Return Value:
        N/A
    '''

    # invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
     
    # invalid channel_id
    if not check_valid_channel_id(channel_id):
        raise InputError(description = 'Channel id is not valid')

    # No owner permission
    if not check_channel_owner_permission(auth_user_id, channel_id):
        raise AccessError(description ='No owner permission in the channel')
    
    # invalid u_id
    if not channels_create_check_valid_user(u_id):
        raise InputError(description = 'user is not valid')

    # u_id not a member of the channel
    if not check_valid_member_in_channel(channel_id, u_id):
        raise InputError(description = 'User is not a member of the channel')
    
    # u_id already owner of the channel
    if check_valid_owner(u_id, channel_id):
        raise InputError(description = 'User is already an owner of the channel')
   
    user = user_info(u_id)

    for channels in get_data()['channels']:
        channels['owner_members'].append(user)
        save()

    return {}

def channel_removeowner_v1(token, channel_id, u_id):
    '''
    Remove user with user id u_id as an owner of the channel.

    Arguments:
        <token>        (<string>)   - an authorisation hash
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
                    - Occurs when token is invalid

    Return Value:
        N/A
    '''
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    
    # channel_id does not refer to a valid channel
    if not check_valid_channel_id(channel_id) or not isinstance(channel_id, int):
        raise InputError(description = 'The channel_id does not refer to a valid channel')

    # channel_id is valid and the authorised user does not have owner permissions in the channel
    if not check_channel_owner_permission(auth_user_id, channel_id):
        raise AccessError(description = 'No owner permission in the channel')
    
    # u_id does not refer to a valid user
    if not channels_create_check_valid_user(u_id):
        raise InputError(description = 'The u_id does not refer to a valid user')
    
    # u_id refers to a user who is not an owner of the channel
    if not check_valid_owner(u_id, channel_id):
        raise InputError(description = 'The u_id does not refer to a user who is not an owner of the channel')

    # u_id refers to a user who is currently the only owner of the channel
    channel = get_channel_details(channel_id)
    if len(channel['owner_members']) == 1:
        raise InputError(description = 'The u_id refers to a user who is currently the only owner of the channel')
    
    for channel in get_data()['channels']:
        for owner in channel['owner_members']:
            if owner['u_id'] == u_id:
                channel['owner_members'].remove(owner)
                save()
    return {}
