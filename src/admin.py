'''
Admin implementation
'''
from src.error import InputError, AccessError
from src.helper import check_permision_id, channels_create_check_valid_user, check_number_of_owners, check_permission
from src.helper import get_user_details
from src.data_store import get_data, save
from src.server_helper import decode_token, valid_user

def admin_user_remove_v1(token, u_id):
    '''
    Given a user by their u_id, remove them from the Streams. 

    Arguments:
        <token>     (<string>)        - an authorisation hash
        <u_id>      (<int>)         - the unique id of the user

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    - Occurs when u_id refers to a user who is the only global owner
        AccessError - Occurs when the authorised user is not a global owner
                    - Occurs when token is invalid

    Return Value:
        N/A
    '''

    # Access Error when token is invalid
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    auth_user_id = decode_token(token)

    # Access error when the authorised user is not a global owner
    if not check_permision_id(auth_user_id):
        raise AccessError(description='The authorised user is not a global owner')

    # Input error when u_id does not refer to a valid user
    if not channels_create_check_valid_user(u_id):
        raise InputError(description='The u_id does not refer to a valid user')

    # Input error when u_id refers to a user who is the only global owner
    user = check_number_of_owners(u_id)
    if user == 0:
        raise InputError(description='The u_id refers to a user who is the only global owner')

    # remove users from channel
    for channel in get_data()['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
        for owner in channel['owner_members']:
            if owner['u_id'] == u_id:
                channel['owner_members'].remove(owner)
        # replace the message they sent in the channel to be 'Removed user'
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
        save()

    # remove users from dm
    for dm in get_data()['dms']:    
        for member in dm['members']:
            if member['u_id'] == u_id:
                dm['members'].remove(member)
        if len(dm['creator']) > 0:
            if dm['creator']['u_id'] == u_id:
                dm['creator'].clear()
        # replace the message they sent in dm to be 'Removed user'
        for message in dm['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
        save()
    
    # the contents of the messages they sent will be replaced by 'Removed user'
    for message in get_data()['messages']:
        if message['u_id'] == u_id:
            message['message'] = 'Removed user'
        save()

    for user in get_data()['users']:
        if user['auth_user_id'] == u_id:
            # the user will not be included by user/all
            user['is_removed'] = True
            # name_first should be 'Removed' and name_last should be 'user'.
            user['name_first'] = 'Removed'
            user['name_last'] = 'user'
            # user's email and handle is set to be empty 
            # so that it can be reusable.
            user['handle_str'] = ''
            user['email'] = ''
            user['profile_img_url'] = ''
            user['time_stamp'] = ''
            user['all_notifications'] = []
            user['channels_joined'].clear()
            user['dms_joined'].clear()
            user['messages_sent'].clear()
            # invalidate user's token
            user['session_list'].clear()
            save()
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a user by their user ID, set their permissions to new permissions described by permission_id.

    Arguments:
        <token>         (<string>)  - an authorisation hash
        <u_id>          (<int>)     - the unique id of the user
        <permission_id> (<int>)     - the id that refers to the user's permission

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    - Occurs when permission_id is invalid
                    - Occurs when u_id refers to a user who is the only global owner and 
                    they are being demoted to a user
        AccessError - Occurs when the authorised user is not a global owner
                    - Occurs when token is invalid

    Return Value:
        N/A
    '''

    # Access error when token is invalid
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # AccessError when the authorised user is not a global owner
    if not check_permision_id(auth_user_id):
        raise AccessError(description='The authorised user is not a global owner')

    # InputError when u_id does not refer to a valid user
    if not isinstance(u_id, int) or not channels_create_check_valid_user(u_id):
        raise InputError(description='The u_id does not refer to a valid user')
    
    # InputError when u_id refers to a user who is the only global owner 
    # and they are being demoted to a user
    owner = check_number_of_owners(u_id)
    if owner == 0 and not check_permission(u_id, permission_id):
        raise InputError(description='U_id refers to the only global owner and they are being demoted')

    # Input error when permission_id is invalid
    if permission_id < 1 or permission_id > 2:
        raise InputError(description='The permission_id is invalid')

    # update user's permission_id
    user = get_user_details(u_id)
    user['permission_id'] = permission_id
    save()
    return {}
