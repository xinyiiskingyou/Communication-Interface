from src.server_helper import decode_token, valid_user
from src.helper import check_valid_email, channels_user_details, channels_create_check_valid_user
from src.helper import user_info
from src.error import InputError
from src.data_store import DATASTORE, initial_object

def users_all_v1(token): 
    '''
    Returns a list of all users and their associated details.

    Arguments:
        <token>     (<string>)    - an authorisation hash

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user

    Return Value:
        Returns <auth_user_id> of valid user
        Returns <email> of valid user
        Returns <name_first> of valid user
        Returns <name_last> of valid user
        Returns <handle> of valid user
    '''
    store = DATASTORE.get()
    #valid_user(token)
    #decode_token(token)

    user_list = []

    for user in initial_object['users']:
        if user['is_removed'] == False:
            user_list.append(user_info(user['auth_user_id']))
    
    DATASTORE.set(store)
    return (user_list)

def user_profile_v1(token, u_id):
    '''
    For a valid user, returns information about their user_id, email, first name, last name, and handle.

    Arguments:
        <token>     (<string>)    - an authorisation hash
        <u_id>      (<int>)       - an unique auth_user_id of the user to be added as an owner of the channel
        ...

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user

    Return Value:
        Returns <auth_user_id> of valid user
        Returns <email> of valid user
        Returns <name_first> of valid user
        Returns <name_last> of valid user
        Returns <handle> of valid user
    '''
    valid_user(token)

    if not channels_create_check_valid_user(int(u_id)):
        raise InputError(description='The u_id does not refer to a valid user')
    return (user_info(int(u_id)))

def user_profile_setname_v1(token, name_first, name_last):
    '''
    Update the authorised user's first and last name

    Arguments:
        <token>         (<string>)    - an authorisation hash
        <name_first>    (<string>)    - alphanumerical first name
        <name_last>     (<string>)    - alphanumerical first name
        ...

    Exceptions:
        InputError  - Occurs when length of name_first is not between 1 and 50 characters inclusive
                    - Occurs when length of name_last is not between 1 and 50 characters inclusive

    Return Value:
        Returns N/A
    '''

    store = DATASTORE.get()
    # Invalid first name
    if len(name_first) not in range(1, 51):
        raise InputError(description='name_first is not between 1 - 50 characters in length')

    # Invalid last name
    if len(name_last) not in range(1, 51):
        raise InputError(description='name_last is not between 1 - 50 characters in length')

    auth_user_id = decode_token(token)
    user = channels_user_details(auth_user_id)
    user['name_first'] = name_first
    user['name_first'] = name_last
    DATASTORE.set(store)
    return {}

def user_profile_setemail_v1(token, email):
    '''
    Update the authorised user's email address.

    Arguments:
        <token>     (<string>)      - an authorisation hash
        <email>     (<string>)    - email user used to register into Streams

    Exceptions:
        InputError  - Occurs when email entered is not a valid email
                    - Occurs when email address is already being used by another user

    Return Value:
        Returns N/A
    '''

    valid_user(token)
    auth_user_id = decode_token(token)

    store = DATASTORE.get()
    # email entered is not a valid email
    if not check_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    # email address is already being used by another user
    for users in initial_object['users']:
        if users['email'] == email:
            raise InputError(description='Email address is already being used by another user')

    auth_user_id = decode_token(token)
    user = channels_user_details(auth_user_id)
    user['email'] = email
    DATASTORE.set(store)
    return {}

def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name).

    Arguments:
        <token>          (<string>)      - an authorisation hash
        <handle_str>     (<string>)    - the concatenation of user's first name and last name

    Exceptions:
        InputError  - Occurs when length of handle_str is not between 3 and 20 characters inclusive
                    - Occurs when handle_str contains characters that are not alphanumeric
                    - Occurs when the handle is already used by another user

    Return Value:
        Returns N/A
    '''

    valid_user(token)
    auth_user_id = decode_token(token)

    store = DATASTORE.get()

    # length of handle_str is not between 3 and 20 characters inclusive
    if len(handle_str) not in range(3, 21):
        raise InputError(description='handle_str is not between 1 - 20 characters in length')

    # handle_str contains characters that are not alphanumeric
    if not handle_str.isalnum():
        raise InputError(description='handle_str contains characters that are not alphanumeric')

    # the handle is already used by another user
    for users in initial_object['users']:
        if users['handle_str'] == handle_str:
             raise InputError(description='The handle is already used by another user')

    auth_user_id = decode_token(token)
    user = channels_user_details(auth_user_id)
    user['handle_str'] = handle_str
    DATASTORE.set(store)
    return {}
