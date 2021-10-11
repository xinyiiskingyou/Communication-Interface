from src.error import InputError, AccessError
from src.helper import *
from src.data_store import DATASTORE, initial_object
from src.server_helper import decode_token

def admin_user_remove_v1(token, u_id):

    # u_id does not refer to a valid user
    if not isinstance(u_id, int) or not channels_create_check_valid_user(u_id):
        raise InputError("The u_id does not refer to a valid user")

    # u_id refers to a user who is the only global owner
    if check_permision_id(u_id):
        raise InputError("The u_id refers to a user who is the only global owner")

    # the authorised user is not a global owner
    if not check_permision_id(u_id):
        raise AccessError('The authorised user is not a global owner')


    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a user by their user ID, set their permissions to new permissions described by permission_id.
    '''
    store = DATASTORE.get()

    auth_user_id = decode_token(token)
    user = channels_user_details(u_id)
    # u_id does not refer to a valid user
    if not isinstance(u_id, int) or not channels_create_check_valid_user(u_id):
        raise InputError("The u_id does not refer to a valid user")
    
    # u_id refers to a user who is the only global owner and they are being demoted to a user

    # permission_id is invalid
    if permission_id < 1 or permission_id > 2:
        raise InputError("The permission_id is invalid")

    # the authorised user is not a global owner
    if not check_permision_id(auth_user_id):
        raise AccessError

    user['permission_id'] = permission_id
    DATASTORE.set(store)
    return {}
