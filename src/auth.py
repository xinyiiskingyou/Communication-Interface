'''
Auth implementation
'''
import re
import string
import random
import smtplib 
import hashlib
import time
import urllib.request
from src.data_store import get_data, save
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

    # Iterate through the users list
    for user in get_data()['users']:
        # If the email and password the user inputs to login match and exist in data_store
        if (user['email'] == email) and (user['password'] == hashlib.sha256(password.encode()).hexdigest()):
            session_id = generate_sess_id()
            user['session_list'].append(session_id)
            auth_user_id = user['auth_user_id']
            save()
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

    # Access error when token in invalid
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    session_id = decode_token_session_id(token)
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            # invalidate the user's token and session_id
            user['session_list'].remove(session_id)
            save()

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

    # Error handling
    search = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if not re.search(search, email):
        raise InputError(description='This email is of invalid form')

    # Check for duplicate emails
    for user in get_data()['users']:
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
    auth_user_id = len(get_data()['users']) + 1

    session_id = generate_sess_id()
    token = generate_token(auth_user_id, session_id)

    password = hashlib.sha256(password.encode()).hexdigest() 
    reset_code = ''

    # Creating handle and adding to dict_user
    handle = (name_first + name_last).lower()
    handle = re.sub(r'[^a-z0-9]', '', handle)
    if len(handle) > 20:
        handle = handle[0:20]

    new_len = len(handle)

    # Check for duplicate handles
    num_dup = 0
    i = 0
    while i < len(get_data()['users']):
        user = get_data()['users'][i]
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

    # all the users are not be removed when they register
    is_removed = False
    # the time when the account create
    time_created = int(time.time())

    # Deafult profile photo
    img_url = "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg"
    img_name = "static/default_pic"
    urllib.request.urlretrieve(img_url, img_name)

    # Then append dictionary of user email onto initial_objects
    get_data()['users'].append({
        'email' : email,
        'password': password,
        'name_first': name_first,
        'name_last' : name_last,
        'session_list': [session_id],
        'auth_user_id' : int(auth_user_id),
        'handle_str' : handle,
        'permission_id' : permission_id,
        'is_removed': bool(is_removed),
        'reset_code': reset_code,
        'time_stamp': time_created,
        'all_notifications': [],
        'profile_img_url': img_name
    })
    save()

    return {
        'token': token,
        'auth_user_id': auth_user_id
    }

def auth_passwordreset_request_v1(email):
    '''
    Given a user's email address, if they are a registered user, sends an email containing a
    reset code to passwordrequest_reset that when entered into the passwordrequest_reset function,
    shows that the user trying to reset the password is the one who got sent the email

    Arguments:
        <email>      (<string>)    - correct format of an email of the user

    Exceptions:
        N/A

    Return Value:
        Returns <{}> when user successfully requests a password reset
    '''
    reset_code = ''.join(random.choice(string.ascii_uppercase + string.ascii_letters) for i in range(20)) 
    # Get valid user
    for user in get_data()['users']:
        if user['email'] == email:
            # Assign reset code
            user['reset_code'] = reset_code

            # Send email
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('camel5363885@gmail.com', 'camel_password!')
            mail.sendmail('camel5363885@gmail.com', email, reset_code)
            mail.close

            # Log them out of all sessions
            user['session_list'].clear
            save()
   
    return {}

def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
    Given a reset code for a user, set that user's new password to the password provided

    Arguments:
        <reset_code>      (<string>)    - random length of string 20 consisting of uppercase
                                        and lowercase letters

    Exceptions:
        InputError  - Occurs when reset_code entered is not valid
                    - Occurs when new_password entered is < 6 characters in length 

    Return Value:
        Returns <{}> when user successfully changes password
    '''

    # Invalid password length
    if len(new_password) in range(6):
        raise InputError(description='Password entered is less then  6 characers in length')
   
    # Get valid user
    correct_user = None
    for user in get_data()['users']:
        if user['reset_code'] == reset_code:
            correct_user = user
            break

    # Invalid reset_code
    if correct_user is None:
        raise InputError(description='Invalid reset_code')

    # Hashing new password and setting reset code to empty string
    new_password = hashlib.sha256(new_password.encode()).hexdigest() 
    user['password'] = new_password
    user['reset_code'] = ''
    save()
    return {}
