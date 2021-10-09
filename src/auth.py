'''
Auth implementation
'''
import re
import hashlib
from src.data_store import DATASTORE, initial_object
from src.error import InputError
from src.server_helper import generate_token

def auth_login_v1(email, password):
    '''
    Given a registered user's email and password, returns their `auth_user_id` value.

    Arguments:
        <email>     (<string>)    - email user used to register into Streams
        <password>  (<string>)    - password user used to register into Streams

    Exceptions:
        InputError  - Occurs when email entered does not belong to a user
                    - Occurs when password is not correct

    Return Value:
        Returns <{auth_user_id}> when user successfully logins into Streams
    '''

    # Iterate through the initial_object list
    for user in initial_object['users']:
        # If the email and password the user inputs to login match and exist in data_store
        if (user['email'] == email) and (user['password'] == password):
            auth_user_id = user['auth_user_id']
            return {
                'auth_user_id': auth_user_id
            }
    raise InputError("Email and/or password is not valid!")

def auth_register_v2(email, password, name_first, name_last):
    '''
    Given a user's first and last name, email address, and password,
    create a new account for them and return a new `auth_user_id`.

    Arguments:
        <email>      (<string>)    - correct format of an email of the user
        <password>   (<string>)    - password user used to register into Streams
        <name_first> (<string>)    - alphanumerical first name
        <name_last>  (<string>)    - alphanumerical last name
        ...

    Exceptions:
        InputError  - Occurs when email entered is not a valid email
                    - Occurs when email address is already being used by another user
                    - Occurs when length of password is less than 6 characters
                    - Occurs when length of name_first is not between 1 and 50 characters inclusive
                    - Occurs when length of name_last is not between 1 and 50 characters inclusive

    Return Value:
        Returns <{auth_user_id}> when user successfully creates a new account in Streams
    '''

    store = DATASTORE.get()

    # Error handling
    search = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if not re.search(search, email):
        raise InputError("This email is of invalid form")

    # Check for duplicate emails
    for user in initial_object['users']:
        if user['email'] == email:
            raise InputError("This email address has already been registered by another user")

    # Valid Password
    if len(password) < 6:
        raise InputError("This password is less then 6 characters in length")

    # Valid first name
    if len(name_first) not in range(1, 51):
        raise InputError("name_first is not between 1 - 50 characters in length")

    # Valid last name
    if len(name_last) not in range(1, 51):
        raise InputError("name_last is not between 1 - 50 characters in length")

    # Creating unique auth_user_id and hashing and encoding the token and password
    auth_user_id = len(initial_object['users']) + 1
    token = generate_token(auth_user_id)

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

    # Then append dictionary of user email onto initial_objects
    initial_object['users'].append({
        'email' : email,
        'password': password,
        'name_first': name_first,
        'name_last' : name_last,
        'token': token,
        'auth_user_id' : auth_user_id,
        'handle_str' : handle,
        'permission_id' : permission_id
    })

    DATASTORE.set(store)
    return {
        'token': token,
        'auth_user_id': auth_user_id
    }

