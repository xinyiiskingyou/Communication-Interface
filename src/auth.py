'''
Auth implementation
'''
import re
import hashlib
from src.data_store import DATASTORE, initial_object
from src.error import InputError, AccessError
from src.server_helper import generate_token, generate_sess_id
from src.server_helper import decode_token, decode_token_session_id, valid_user

def auth_login_v2(email, password):
    '''
    Given a registered user's email and password, returns their `auth_user_id` value.

    Arguments:
        <email>     (<string>)    - email user used to register into Streams
        <password>  (<string>)    - password user used to register into Streams

    Exceptions:
        InputError  - Occurs when email entered does not belong to a user
                    - Occurs when password is not correct

    Return Value:
        Returns <{auth_user_id, token}> when user successfully logins into Streams
    '''

    # Iterate through the initial_object list
    for user in initial_object['users']:
        # If the email and password the user inputs to login match and exist in data_store
        if (user['email'] == email) and (user['password'] == hashlib.sha256(password.encode()).hexdigest()):
            session_id = generate_sess_id()
            user['session_list'].append(session_id)
            auth_user_id = user['auth_user_id']
            return {
                'token': generate_token(auth_user_id, session_id),
                'auth_user_id': auth_user_id
            }
    raise InputError(description='Email and/or password is not valid!')

def auth_logout_v1(token):
    '''
    Given an active token, invalidates the token to log the user out.

    Arguments:
        <token> (<string>)    - an authorisation hash

    Exceptions:
        AccessError  - Occurs when token is invalid

    Return Value:
        N/A
    '''
    store = DATASTORE.get()

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    session_id = decode_token_session_id(token)
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            user['session_list'].remove(session_id)

    DATASTORE.set(store)
    return {}


def auth_register_v2(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password,
    create a new account for them and return a new `auth_user_id`.

    Arguments:
        <email>      (<string>)    - correct format of an email of the user
        <password>   (<string>)    - password user used to register into Streams
        <name_first> (<string>)    - alphanumerical first name
        <name_last>  (<string>)    - alphanumerical last name

    Exceptions:
        InputError  - Occurs when email entered is not a valid email
                    - Occurs when email address is already being used by another user
                    - Occurs when length of password is less than 6 characters
                    - Occurs when length of name_first is not between 1 and 50 characters inclusive
                    - Occurs when length of name_last is not between 1 and 50 characters inclusive

    Return Value:
        Returns <{auth_user_id, token}> when user successfully creates a new account in Streams
    '''

    store = DATASTORE.get()

    # Error handling
    search = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if not re.search(search, email):
        raise InputError(description='This email is of invalid form')

    # Check for duplicate emails
    for user in initial_object['users']:
        if user['email'] == email:
            raise InputError(description='This email address has already been registered')

    # Valid Password
    if len(password) < 6:
        raise InputError(description='This password is less then 6 characters in length')

    # Valid first name
    if len(name_first) not in range(1, 51):
        raise InputError(description='name_first is not between 1 - 50 characters in length')

    # Valid last name
    if len(name_last) not in range(1, 51):
        raise InputError(description='name_last is not between 1 - 50 characters in length')

    # Creating unique auth_user_id and hashing and encoding the token and password
    auth_user_id = len(initial_object['users']) + 1

    session_id = generate_sess_id()
    token = generate_token(auth_user_id, session_id)

    password = hashlib.sha256(password.encode()).hexdigest() 

    # Creating handle and adding to dict_user
    handle = (name_first + name_last).lower()
    handle = re.sub(r'[^a-z0-9]', '', handle)
    if len(handle) > 20:
        handle = handle[0:20]

    new_len = len(handle)

    # Check for duplicate handles
    num_dup = 0
    i = 0
    while i < len(initial_object['users']):
        user = initial_object['users'][i]
        if user['handle_str'] == handle:
            handle = handle[0:new_len]
            handle = handle[0:20] + str(num_dup)
            num_dup += 1
            i = 0
        else:
            i += 1

    # Permission id for streams users
    if auth_user_id == 1:
        permission_id = 1
    else:
        permission_id = 2

    is_removed = False
    # Then append dictionary of user email onto initial_objects
    initial_object['users'].append({
        'email' : email,
        'password': password,
        'name_first': name_first,
        'name_last' : name_last,
        'session_list': [session_id],
        'auth_user_id' : int(auth_user_id),
        'handle_str' : handle,
        'permission_id' : permission_id,
        'is_removed': bool(is_removed),
    })

    DATASTORE.set(store)
    return {
        'token': token,
        'auth_user_id': auth_user_id
    }

