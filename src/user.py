'''
User implementation
'''
import time
import requests
import urllib.request
from PIL import Image
from flask import url_for
from src.server_helper import decode_token, valid_user
from src.helper import check_valid_email, channels_create_check_valid_user
from src.helper import user_info, get_channel_details, get_dm_dict, get_user_details
from src.helper import check_join_channel_or_dm, get_messages_total_number, get_current_user
from requests.api import get
from src.error import AccessError, InputError
from src.data_store import get_data, save
from src.config import url

def users_all_v1(token): 
    '''
    Returns a list of all users and their associated details.

    Arguments:
        <token>     (<string>)    - an authorisation hash

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
        AccessError - Occurs when token is invalid

    Return Value:
        Returns <auth_user_id> of valid user
        Returns <email> of valid user
        Returns <name_first> of valid user
        Returns <name_last> of valid user
        Returns <handle> of valid user
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    user_list = []
    for user in get_data()['users']:
        if user['is_removed'] == False:
            user_list.append(user_info(user['auth_user_id']))

    return {
        'users': (user_list)
    }

def users_stats_v1(token):
    '''
    Fetches the required statistics about the use of UNSW Streams.

    Arguments:
        <token>          (<string>)      - an authorisation hash

    Exceptions:
        N/A

    Return Value:
        <work_space_stats> (<dict>)     - stores the channels_exist, dms_exist, 
                                          messages_exist and utilization rate
    '''
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    # get the number of users in the stream
    users = get_data()['users']
    num_users = 0
    for user in users:
        if user['is_removed'] == False:
            num_users += 1
    
    num_users_joined_atleast_one_channel_or_dm = 0

    # for every user, check if they join at least one channel or dm
    for i in range(len(users)):
        if users[i]['is_removed'] == False:
            if check_join_channel_or_dm(users[i]['auth_user_id']):
                num_users_joined_atleast_one_channel_or_dm += 1
            
    # compute utilization rate
    utilization_rate = 0.0
    if num_users != 0 and num_users_joined_atleast_one_channel_or_dm != 0:
        utilization_rate = float(num_users_joined_atleast_one_channel_or_dm) / float(num_users)

    get_data()['workspace_stats']['utilization_rate'] = float(utilization_rate)
    save()
    return {
        'workspace_stats': get_data()['workspace_stats']
    }

def user_stats_v1(token):
    '''
    Fetches the required statistics about this user's use of UNSW Streams.

    Arguments:
        <token>     (<string>)    - an authorisation hash

    Exceptions:
        AccessError - Occurs when token is invalid

    Return Value:
        Returns a dictionary of shape {
             channels_joined: [{num_channels_joined, time_stamp}],
             dms_joined: [{num_dms_joined, time_stamp}], 
             messages_sent: [{num_messages_sent, time_stamp}], 
             involvement_rate 
        }
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    user = get_user_details(auth_user_id)

    # get the total number of channels
    num_channels = len(get_data()['channels'])
    channel_length = len(user['channels_joined'])
    # get the number of channels that the user joined
    num_channels_joined = user['channels_joined'][channel_length - 1]['num_channels_joined']

    # get the total number of dms
    num_dms = len(get_data()['dms'])
    dm_length = len(user['dms_joined'])
    # get the number of dms that the user joined
    num_dms_joined = user['dms_joined'][dm_length - 1]['num_dms_joined']

    # get the total number of messages
    num_msgs = get_messages_total_number()
    msg_length = len(user['messages_sent'])
    # get the number of messages that the user sent
    num_msgs_sent = user['messages_sent'][msg_length - 1]['num_messages_sent']
            
    try:
        user_sum = num_msgs_sent + num_channels_joined + num_dms_joined
        denominator = num_msgs + num_dms + num_channels
        involvement_rate = user_sum / denominator
    # raise exception when denominator is zero
    except ZeroDivisionError:
        involvement_rate = 0 
    
    # if the involvement is greater than 1, it should be capped at 1.
    if involvement_rate > 1:
        involvement_rate = 1

    return {
        'user_stats': {
            'channels_joined': user['channels_joined'],
            'dms_joined': user['dms_joined'],
            'messages_sent': user['messages_sent'],
            'involvement_rate': float(involvement_rate)
        }
    }

def user_profile_v1(token, u_id):
    '''
    For a valid user, returns information about their user_id, email, first name, last name, and handle.

    Arguments:
        <token>     (<string>)    - an authorisation hash
        <u_id>      (<int>)       - an unique auth_user_id of the user to be added as an owner of the channel

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
        AccessError - Occurs when token is invalid

    Return Value:
        Returns <auth_user_id> of valid user
        Returns <email> of valid user
        Returns <name_first> of valid user
        Returns <name_last> of valid user
        Returns <handle> of valid user
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    if not channels_create_check_valid_user(int(u_id)):
        raise InputError(description='The u_id does not refer to a valid user')
    return {
        'user': user_info(int(u_id))
    }

def user_profile_setname_v1(token, name_first, name_last):
    '''
    Update the authorised user's first and last name

    Arguments:
        <token>         (<string>)    - an authorisation hash
        <name_first>    (<string>)    - alphanumerical first name
        <name_last>     (<string>)    - alphanumerical first name

    Exceptions:
        InputError  - Occurs when length of name_first is not between 1 and 50 characters inclusive
                    - Occurs when length of name_last is not between 1 and 50 characters inclusive
        AccessError - Occurs when token is invalid

    Return Value:
        Returns N/A
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    # Invalid first name
    if len(name_first) not in range(1, 51):
        raise InputError(description='name_first is not between 1 - 50 characters in length')

    # Invalid last name
    if len(name_last) not in range(1, 51):
        raise InputError(description='name_last is not between 1 - 50 characters in length')

    auth_user_id = decode_token(token)
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            user['name_first'] = name_first
            user['name_last'] = name_last
            save()
    
    # change user's first name and last name in channel
    for channel in get_data()['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                member['name_first'] = name_first
                member['name_last'] = name_last
        for owner in channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                owner['name_first'] = name_first
                owner['name_last'] = name_last  
        save()    

    # change user's first name and last name in dm
    for dm in get_data()['dms']:
        for member in dm['members']:
            if member['u_id'] == auth_user_id:
                member['name_first'] = name_first
                member['name_last'] = name_last    
        if len(dm['creator']) > 0:
            if dm['creator']['u_id'] == auth_user_id:
                dm['creator']['name_first'] = name_first
                dm['creator']['name_last'] = name_last  
        save()

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
        AccessError - Occurs when token is invalid

    Return Value:
        Returns N/A
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    # email entered is not a valid email
    if not check_valid_email(email):
        raise InputError(description='Email entered is not a valid email')

    # email address is already being used by another user
    for users in get_data()['users']:
        if users['email'] == email:
            raise InputError(description='Email address is already being used by another user')

    auth_user_id = decode_token(token)
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            user['email'] = email
            save()

    # change user's first name and last name in channel
    for channel in get_data()['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                member['email'] = email
        for owner in channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                owner['email'] = email
        save()

    # change user's first name and last name in dm
    for dm in get_data()['dms']:
        for member in dm['members']:
            if member['u_id'] == auth_user_id:
                member['email'] = email  
        if len(dm['creator']) > 0:
            if dm['creator']['u_id'] == auth_user_id:
                dm['creator']['email'] = email
        save()

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
        AccessError - Occurs when token is invalid
    Return Value:
        Returns N/A
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # length of handle_str is not between 3 and 20 characters inclusive
    if len(handle_str) not in range(3, 21):
        raise InputError(description='handle_str is not between 3 - 21 characters in length')

    # handle_str contains characters that are not alphanumeric
    if not handle_str.isalnum():
        raise InputError(description='handle_str contains characters that are not alphanumeric')

    # the handle is already used by another user
    for users in get_data()['users']:
        if users['handle_str'] == handle_str:
             raise InputError(description='The handle is already used by another user')

    auth_user_id = decode_token(token)

    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            user['handle_str'] = handle_str
            save()

    # change user's first name and last name in channel
    for channel in get_data()['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                member['handle_str'] = handle_str
        for owner in channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                owner['handle_str'] = handle_str
        save()
    
    # change user's first name and last name in dm
    for dm in get_data()['dms']:
        for member in dm['members']:
            if member['u_id'] == auth_user_id:
                member['handle_str'] = handle_str
        if len(dm['creator']) > 0:
            if dm['creator']['u_id'] == auth_user_id:
                dm['creator']['handle_str'] = handle_str
        save()
    return {}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Update the authorised user's handle (i.e. display name).

    Arguments:
        <token>          (<string>)      - an authorisation hash
        <img_url>        (<string>)      - the url of an image 
        <x_start>        (<int>)         - a boundary for the image  
        <y_start>        (<int>)         - a boundary for the image   
        <x_end>          (<int>)         - a boundary for the image   
        <y_end>          (<int>)         - a boundary for the image  

    Exceptions:
        InputError  - Occurs when img_url returns a status other then 200
                    - Occurs when any of x/y_start and x/y_end are not within the dimensions
                    of the image at the url
                    - Occurs when the x/y_end is less then either x_start or y_start
                    - Occurs when image uploaded is not JPG
    Return Value:
        Returns N/A
    '''
    # Access Error: invalid token
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Input Error: img_url returns a status code other then 200 -> REDO IMPLEMENTATION
    try:
        requests.get(img_url, stream=True).status_code != 200
    except Exception as invalid_url:
        raise InputError(description='invalid url') from invalid_url

    # Input Error: image is not JPG
    if not img_url.lower().endswith('.jpg'):
        raise InputError(description='img_url is not of type JPG.')

    # Creating unique img url
    updated_time = str(time.time())
    img_name = 'src/static/' + token + updated_time + '.jpg'
    urllib.request.urlretrieve(img_url, img_name)
    imageObject = Image.open(img_name)
    width, height = imageObject.size

    # Check within given boundaries
    if x_start not in range(x_end) or y_start not in range(y_end) or x_end not in range(width + 1) or y_end not in range(height + 1):
        raise InputError(description='Any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL')

    # Cropping img to given dimensions
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_name, 'JPEG')
    new_url = url + 'static/' + token + updated_time + '.jpg' 
    
    user = get_user_details(auth_user_id)
    user['profile_img_url'] = new_url
    save()

    for channel in get_data()['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                member['profile_img_url'] = new_url
        for owner in channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                owner['profile_img_url'] = new_url
        save()
    
    for dm in get_data()['dms']:
        for member in dm['members']:
            if member['u_id'] == auth_user_id:
                member['profile_img_url'] = new_url
        if len(dm['creator']) > 0:
            if dm['creator']['u_id'] == auth_user_id:
                dm['creator']['profile_img_url'] = new_url
        save()

    return {}
