'''
User implementation
'''
import urllib.request
from PIL import Image
from src.config import url
from src.server_helper import decode_token, valid_user
from src.helper import check_valid_email, channels_create_check_valid_user
from src.helper import user_info, get_channel_details, get_dm_dict, get_user_details
from src.error import AccessError, InputError
from src.data_store import get_data, save

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

def user_stats_v1(token):

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    
    # the first data point is 0 and 
    # the time_stamp is the time that their account was created
    channels_joined_details = {
        'num_channels_joined': 0,
        'time_stamp': get_user_details(auth_user_id)['time_stamp']
    }
    channels_joined = [channels_joined_details]
    num_channels_joined = 0
    num_channels = 0
    for channel in get_data()['channels']:
        # get the total number of existed channels
        num_channels += 1
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                num_channels_joined += 1
                channels_joined.append({
                    'num_channels_joined': num_channels_joined,
                    'time_stamp': get_channel_details(channel['channel_id'])['time_stamp']
                })

    dms_joined = []
    num_dms_joined = 0
    num_dms = 0
    # the first data point is 0 and 
    # the time_stamp is the time that their account was created
    dms_joined_details = {
        'num_dms_joined': 0,
        'time_stamp': get_user_details(auth_user_id)['time_stamp']
    }
    dms_joined = [dms_joined_details]
    for dm in get_data()['dms']:
        # get the total number of existed dms
        num_dms += 1
        for member in dm['members']:
            if member['u_id'] == auth_user_id:
                num_dms_joined += 1
                dms_joined.append({
                    'num_dms_joined': num_dms_joined,
                    'time_stamp': get_dm_dict(dm['dm_id'])['time_stamp']
                })

    # the first data point is 0 and 
    # the time_stamp is the time that their account was created
    messages_sent_details = {
        'num_messages_sent': 0,
        'time_stamp': get_user_details(auth_user_id)['time_stamp']
    }
    messages_sent = [messages_sent_details]
    num_msgs_sent = 0
    num_msgs = 0
    for message in get_data()['messages']:
        # get the total number of existed messages
        num_msgs += 1
        if message['u_id'] == auth_user_id:
            # get the number of message that the user sent
            num_msgs_sent += 1
            messages_sent.append({
                'num_messages_sent': num_msgs_sent,
                'time_stamp': message['time_created']
            })
    
    try:
        user_sum = num_msgs_sent + num_channels_joined + num_dms_joined
        denominator = num_msgs + num_dms + num_channels
        involvement_rate = user_sum / denominator
    except ZeroDivisionError:
        involvement_rate = 0 

    if involvement_rate > 1:
        involvement_rate = 1

    return {
        'user_stats': {
            'channels_joined': channels_joined,
            'dms_joined': dms_joined,
            'messages_sent': messages_sent,
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
    if urllib.request.urlopen(img_url).getcode() == False:
        raise InputError(description='img_url returns an HTTP status other than 200.')

    # Input Error: image is not JPG
    if not img_url.lower().endswith('.jpg'):
        raise InputError(description='img_url is not of type JPG.')

    # Creating unique img url
    img_name = 'static/' + token + '.jpg'
    urllib.request.urlretrieve(img_url, img_name)
    imageObject = Image.open(img_name)
    width, height = imageObject.size

    # Check within given boundaries
    if x_start not in range(x_end) or y_start not in range(y_end) or x_end not in range(width + 1) or y_end not in range(height + 1):
        raise InputError(description='Any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL')

    # Cropping img to given dimensions
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img_name)
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            user['profile_img_url'] = url + img_name
            save()

    for channel in get_data()['channels']:
        for member in channel['all_members']:
            if member['u_id'] == auth_user_id:
                member['profile_img_url'] = user['profile_img_url']
        for owner in channel['owner_members']:
            if owner['u_id'] == auth_user_id:
                owner['profile_img_url'] = user['profile_img_url']
    return {}

