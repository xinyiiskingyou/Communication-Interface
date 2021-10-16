'''
Helper functions
'''
import re
from src.data_store import initial_object

#Helper function for channels_create, channel_invite, channel_join
#Helper function to return the specific details of users

def user_info(auth_user_id):
    '''
    return type: dict
    '''
    user = channels_user_details(auth_user_id)
    return {
        'u_id': auth_user_id,
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str']
    }

#################################################
####### Helper functions for channels.py ########
#################################################

# Helper function for channel_list, channel_listall, channel_create
# Checks if the auth_user_id given is registered
# Returns true if auth_user_id is registered in streams
# Returns false if not registered
def channels_create_check_valid_user(auth_user_id):
    '''
    return type: bool
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return True
    return False


# Helper function for helper user_info
# Access the details of the given auth_user_id
# Returns the specific dictionary of one user
def channels_user_details(auth_user_id):
    '''
    return type: dict
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return user
    return {}


#################################################
######## Helper functions for channel.py ########
#################################################

# Helper function for channel_messages
# Checks if the start index that is inputted by user is valid or not
# Returns true for valid input
# Returns false for invalid input
def check_valid_start(num_messages, start):
    '''
    return type: bool
    '''
    if not isinstance(start, int):
        return False
    if start > num_messages:
        return False
    if start < 0:
        return False
    return True

# Helper function for channel_details
# Checks if a valid channel_id is being passed in or not
# If valid channel, returns the detail of the channel
def get_channel_details(channel_id):
    '''
    return type: dict
    '''
    for channel in initial_object['channels']:
        if int(channel['channel_id']) == int(channel_id):
            return channel
    return False

# Helper function for channel_invite, channel_details,
# channel_messages and channel_join
# Checks if a valid channel_id is being passed in or not
# Returns true if valid channel
# Returns false otherwise
def check_valid_channel_id(channel_id):
    '''
    return type: bool
    '''
    for channel in initial_object['channels']:
        if int(channel_id) == int(channel['channel_id']):
            return True

    return False

# Helper function for channel_invite, channel_details,
# channel_messages and channel_join
# Checks if the authorised user is a current member of the channel
# Returns true if they are a member
# Returns false otherwise
def check_valid_member_in_channel(channel_id, auth_user_id):
    '''
    return type: bool
    '''

    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    return True
    return False


# Helper function for channel_join
# Checks if the channel is public or private
# Returns true if private channel
# Returns false if public channel
def check_channel_private(channel_id):
    '''
    return type: bool
    '''
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            if not channels['is_public']:
                return True
    return False

# Helper function for channel_join
# Check if authorised user is a global owner of streams
# Returns true if they are a global owner
# Returns false otherwise
def check_permision_id(auth_user_id):
    '''
    return type: bool
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            # If the user is a global owner
            if user['permission_id'] == 1:
                return True
    return False

# checking if the user is an owner
def check_valid_owner(auth_user_id, channel_id):
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            for member in channels['owner_members']:
                if member['u_id'] == auth_user_id:
                    return True
    return False

def check_only_owner(auth_user_id, channel_id):
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            for member in channels['owner_members']:
                if member['u_id'] == auth_user_id:
                    return channels
    pass

def check_global_owner(auth_user_id):
    for user in initial_object['users']:
        if user['auth_user_id'] != auth_user_id:
            continue
        if user['permission_id'] == 1:
            return True
    return False

# checking valid email
def check_valid_email(email):
    '''
    check if the email is valid
    '''
    search = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if re.search(search, email):
        return True
    return False

def check_number_of_owners(u_id):
    number = 0
    for user in initial_object['users']:
        if user['auth_user_id'] == u_id:
            continue
        if user['permission_id'] == 1:
            number += 1
    return number

def check_permission(u_id, permission_id):

    for user in initial_object['users']:
        if user['auth_user_id'] != u_id:
            continue
        # If the user is a global owner
        if permission_id == 1:
            return True
    return False

def check_valid_owner(auth_user_id, channel_id):
    for channels in initial_object['channels']:
        if channels['channel_id'] == channel_id:
            for member in channels['owner_members']:
                if member['u_id'] == auth_user_id:
                    return True
    return False

# get the handle of the authorised user
def get_handle(auth_user_id):
    '''
    return type: <string>
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return user['handle_str']
    return None

# get the dm info of which the auth user is a member of
def get_dm_info(auth_user_id):
    '''
    return type: list
    '''
    dms = []
    handle = get_handle(auth_user_id)
    for dm in initial_object['dms']:
        find = dm['name'].find(handle)
        if find != -1:
            dms.append(dm)
    return dms

# check if the user is the creator of the given dm
def check_creator(auth_user_id, dm_id):
    '''
    return type: bool
    '''
    for dm in initial_object['dms']:
        if dm['dm_id'] != dm_id:
            continue
        if dm['creator']['u_id'] == auth_user_id:
            return True
    return False

# check valid dm
def check_valid_dm(dm_id):
    '''
    return type: bool
    '''
    for dm in initial_object['dms']:
        if dm['dm_id'] == dm_id:
            return True
    return False

# return a dictionary of dm with given dm_id
def get_dm_dict(dm_id):
    '''
    return type: dictionary
    '''
    for dm in initial_object['dms']:
        if dm['dm_id'] == dm_id:
            return dm
    return {}
