from src.server_helper import decode_token
from src.helper import check_valid_email, channels_user_details, user_info
from src.error import InputError
from src.data_store import DATASTORE, initial_object

def users_all_v1(token, u_id): 
    return {}

def user_profile_v1(token, u_id):
    '''
    Update the authorised user's email address.

    Arguments:
        <token>     (<hash>)      - an authorisation hash
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
    if not isinstance(u_id, int):
        raise InputError("This is an invalid u_id")
    if not channels_create_check_valid_user(u_id):
        raise InputError("user is not valid")

    auth_user_id = decode_token(token)
    user = user_info(auth_user_id)
    return {
        'user_id': user['auth_user_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
    }

def user_profile_setname_v1(token, name_first, name_last):
    '''
    Update the authorised user's email address.

    Arguments:
        <token>         (<hash>)      - an authorisation hash
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
    # Valid first name
    if len(name_first) not in range(1, 51):
        raise InputError("name_first is not between 1 - 50 characters in length")

    # Valid last name
    if len(name_last) not in range(1, 51):
        raise InputError("name_last is not between 1 - 50 characters in length")

    auth_user_id = decode_token(token)
    user_info(auth_user_id)
    user = channels_user_details(auth_user_id)
    user['name_first'] = name_first
    user['name_first'] = name_last
    DATASTORE.set(store)
    return {}

def user_profile_setemail_v1(token, email):
    '''
    Update the authorised user's email address.

    Arguments:
        <token>     (<hash>)      - an authorisation hash
        <email>     (<string>)    - email user used to register into Streams
        ...

    Exceptions:
        InputError  - Occurs when email entered is not a valid email
                    - Occurs when email address is already being used by another user

    Return Value:
        Returns N/A
    '''
    store = DATASTORE.get()
    # email entered is not a valid email
    if not check_valid_email(email):
        raise InputError('Email entered is not a valid email')

    # email address is already being used by another user
    for users in initial_object['users']:
        if users['email'] == email:
            raise InputError('Email address is already being used by another user')

    auth_user_id = decode_token(token)
    user = channels_user_details(auth_user_id)
    user['email'] = email
    DATASTORE.set(store)
    return {}

def user_profile_sethandle_v1(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name).

    Arguments:
        <token>          (<hash>)      - an authorisation hash
        <handle_str>     (<string>)    - the concatenation of user's first name and last name
        ...

    Exceptions:
        InputError  - Occurs when length of handle_str is not between 3 and 20 characters inclusive
                    - Occurs when handle_str contains characters that are not alphanumeric
                    - Occurs when the handle is already used by another user

    Return Value:
        Returns N/A
    '''
    store = DATASTORE.get()

    # length of handle_str is not between 3 and 20 characters inclusive
    if len(handle_str) not in range(3, 21):
        raise InputError('handle_str is not between 1 - 20 characters in length')

    # handle_str contains characters that are not alphanumeric
    if not handle_str.isalnum():
        raise InputError('handle_str contains characters that are not alphanumeric')

    # the handle is already used by another user
    for users in initial_object['users']:
        if users['handle_str'] == handle_str:
             raise InputError('The handle is already used by another user')

    auth_user_id = decode_token(token)
    user = channels_user_details(auth_user_id)
    user['handle_str'] = handle_str
    DATASTORE.set(store)
    return {}
