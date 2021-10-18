from src.error import InputError, AccessError
from src.helper import *
from src.data_store import DATASTORE, initial_object
from src.server_helper import decode_token

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

    Return Value:
        N/A
    '''
    store = DATASTORE.get()
    auth_user_id = decode_token(token)
    # u_id does not refer to a valid user
    if not channels_create_check_valid_user(u_id):
        # u_id is invalid and authorised user is not a global owner
        if not check_permision_id(auth_user_id):
            raise AccessError(description='The authorised user is not a global owner')
        raise InputError(description='The u_id does not refer to a valid user')

    # u_id refers to a user who is the only global owner
    user = check_number_of_owners(u_id)
    if user == 0:
        # and the authorised user is not a global owner
        if not check_permision_id(auth_user_id):
            raise AccessError(description='The authorised user is not a global owner')
        raise InputError(description='The u_id refers to a user who is the only global owner')

    # the authorised user is not a global owner
    if not check_permision_id(auth_user_id):
        raise AccessError(description='The authorised user is not a global owner')

    # remove users from channel
    for channel in initial_object['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
        for owner in channel['owner_members']:
            if owner['u_id'] == u_id:
                channel['owner_members'].remove(owner)
    
    # remove users from dm
    for dm in initial_object['dms']:
        # remove the name of the user
        handle = get_handle(u_id)
        new_string = dm['name'].replace(handle + ", ", "")
        dm['name'] = new_string
        for member in dm['members']:
            if member['u_id'] == u_id:
                dm['members'].remove(member)
        if dm['creator']['u_id'] == u_id:
            dm['creator'].clear()
    
    #  the contents of the messages they sent will be replaced by 'Removed user'
    for message in initial_object['messages']:
        if message['u_id'] == u_id:
            message['message'] = 'Removed user'

    for user in initial_object['users']:
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

    DATASTORE.set(store)
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a user by their user ID, set their permissions to new permissions described by permission_id.

    Arguments:
        <token>         (<string>)    - an authorisation hash
        <u_id>          (<int>)     - the unique id of the user
        <permission_id> (<int>)     - the id that refers to the user's permission

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    - Occurs when permission_id is invalid
                    - Occurs when u_id refers to a user who is the only global owner and 
                    they are being demoted to a user
        AccessError - Occurs when the authorised user is not a global owner

    Return Value:
        N/A
    '''
    store = DATASTORE.get()

    auth_user_id = decode_token(token)
    user = channels_user_details(u_id)
        
    # u_id does not refer to a valid user
    if not isinstance(u_id, int) or not channels_create_check_valid_user(u_id):
        # if u_id is invalid the authorised user is not a global owner
        if not check_permision_id(auth_user_id):
            raise AccessError(description='The authorised user is not a global owner')
        raise InputError(description='The u_id does not refer to a valid user')
    
    # u_id refers to a user who is the only global owner and they are being demoted to a user
    owner = check_number_of_owners(u_id)
    if owner == 0 and not check_permission(u_id, permission_id):
        # if input error and access error raises at the same time 
        if not check_permision_id(auth_user_id):
            raise AccessError(description='The authorised user is not a global owner')
        raise InputError(description='U_id refers to the only global owner and they are being demoted')

    # permission_id is invalid
    if permission_id < 1 or permission_id > 2:
        # if permission id is invalid and the authorised user is not a global owner
        if not check_permision_id(auth_user_id):
            raise AccessError(description='The authorised user is not a global owner')
        raise InputError(description='The permission_id is invalid')

    # the authorised user is not a global owner
    if not check_permision_id(auth_user_id):
        raise AccessError(description='The authorised user is not a global owner')

    user['permission_id'] = permission_id
    DATASTORE.set(store)
    return {}
