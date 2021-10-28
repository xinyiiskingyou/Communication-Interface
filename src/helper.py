'''
Helper functions
'''
import re
from src.data_store import get_data

#Helper function for channels_create, channel_invite, channel_join
#Helper function to return the specific details of users

def user_info(auth_user_id):
    '''
    return type: dict
    '''
    user = get_user_details(auth_user_id)
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
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            return True
    return False

# Helper function for helper user_info
# Access the details of the given auth_user_id
# Returns the specific dictionary of one user
def get_user_details(auth_user_id):
    '''
    return type: dict
    '''
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            return user

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
    for channel in get_data()['channels']:
        if int(channel['channel_id']) == int(channel_id):
            return channel

# Helper function for channel_invite, channel_details,
# channel_messages and channel_join
# Checks if a valid channel_id is being passed in or not
# Returns true if valid channel
# Returns false otherwise
def check_valid_channel_id(channel_id):
    '''
    return type: bool
    '''
    for channel in get_data()['channels']:
        if int(channel_id) == int(channel['channel_id']):
            return True
    return False

# Helper function for channels_list
# Checks if user is a member of the channel
def get_channel_member(auth_user_id, channel):
    for member in channel['all_members']:
        if member['u_id'] == auth_user_id:
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
    for channel in get_data()['channels']:
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
    for channels in get_data()['channels']:
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
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            # If the user is a global owner
            if user['permission_id'] == 1:
                return True
    return False

# Helper function for channel_join
# Check if the user is an owner of the channel
# Returns true if owner
# Returns false otherwise
def check_valid_owner(auth_user_id, channel_id):

    for channels in get_data()['channels']:
        if channels['channel_id'] == channel_id:
            for member in channels['owner_members']:
                if member['u_id'] == auth_user_id:
                    return True
    return False


# Helper function for channel_removeowner
# Check if there is only one owner left in channel
# Returns true only one owner left
# Returns false otherwise
def check_only_owner(auth_user_id, channel_id):

    for channels in get_data()['channels']:
        if channels['channel_id'] == channel_id:
            for member in channels['owner_members']:
                if member['u_id'] == auth_user_id:
                    return channels


# Helper function for channel_addowner, channel_removeowner
# Checks if auth_user_id is a global owner
# Returns true if global owner
# Returns false otherwise
def check_global_owner(auth_user_id):

    for user in get_data()['users']:
        if user['auth_user_id'] != auth_user_id:
            continue
        if user['permission_id'] == 1:
            return True
    return False


# Helper function for admin_user_remove
# Gets messages of a user in channels
# Returns message if found
# Returns empty dict otherwise
def get_channel_message(u_id, channel):
    for message in channel['messages']:
        if message['u_id'] == u_id:
            return message
    return {}

# Helper function for user_profile_setemail
# Checks valid email
# Returns true if valid
# Returns empty dict otherwise
def check_valid_email(email):
    '''
    check if the email is valid
    '''
    search = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if re.search(search, email):
        return True
    return False

# Helper function for admin_user_remove, admin_userpermisisons_change
# Checks number of owners of a channel
# Returns number
def check_number_of_owners(u_id):
    number = 0
    for user in get_data()['users']:
        if user['auth_user_id'] == u_id:
            continue
        if user['permission_id'] == 1:
            number += 1
    return number

# Helper function for channel_join, admin_user_remove
# Checks permissions of a user
# Returns true if valid
# Returns false otherwise
def check_permission(u_id, permission_id):
    for user in get_data()['users']:
        if user['auth_user_id'] != u_id:
            continue
        # If the user is a global owner
        if permission_id == 1:
            return True
    return False


#################################################
######## Helper functions for message.py ########
#################################################

# Helper function for message_edit_v1
# Checks if message_id refers to a valid message within a channel/DM
# that the authorised user has joined
# Returns true if valid message_id
# Returns false otherwise
def check_valid_message_id(auth_user_id, message_id):
    found_message_id = 0
    channel_dm_id = 0

    # Finds whether or not the message_id exists as a valid message
    if message_id % 2 == 1:
        for channel in get_data()['channels']:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    found_message_id = 1

    if message_id % 2 == 0:
        for dm in get_data()['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    found_message_id = 1

    if found_message_id == 0:
        return False

    # Finds the channel_id or dm_id that message is part of 
    for message in get_data()['messages']:
        if message['message_id'] == message_id:
            if message_id % 2 == 1:
                # Odd message_id means it is a message in a channel
                channel_dm_id = message['channel_id']
            elif message_id % 2 == 0:
                # Even message_id means it is a message in a DM
                channel_dm_id = message['dm_id']
            found_message_id = 1

    # If message_id is odd, message is from channel
    # Go through channels to determine if user is part of channel of that message_id
    found_user = 0
    if message_id % 2 == 1:
        for channel in get_data()['channels']:
            if channel['channel_id'] == channel_dm_id:
                for member in channel['all_members']:
                    if member['u_id'] == auth_user_id:
                        found_user = 1

    # If message_id is odd, message is from DM
    # Go through DMs to determine if user is part of DM of that message_id
    elif message_id % 2 == 0:
        for dm in get_data()['dms']:
            for member in dm['members']:
                if member['u_id'] == auth_user_id:
                    found_user = 1

    # In the case where message being edited is part of a channel, 
    # check if auth_user_id is global owner of Streams
    if message_id % 2 == 1:
        if check_permision_id(auth_user_id):
            found_user = 1

    if found_user == 1 and found_message_id == 1:
        return True
    else:
        return False

# Helper function for message_edit_v1
# Checks if user is authorised to edit message
# Returns true if authorised user
# Returns false otherwise 
def check_authorised_user_edit(auth_user_id, message_id):
    found_message_id = 0
    found_u_id = 0
    channel_dm_id = 0
    # Check message_id is an existing id, and check if u_id of user that 
    # sent the message is the auth_user_id
    for message in get_data()['messages']:
        if message['message_id'] == message_id:
            found_message_id = 1
            if message_id % 2 == 1:
                # Odd message_id means it is a message in a channel
                channel_dm_id = message['channel_id']
            elif message_id % 2 == 0:
                # Even message_id means it is a message in a DM
                channel_dm_id = message['dm_id']

            if message['u_id'] == auth_user_id:
                found_u_id = 1

    # Message_id refers to a valid message in joined channel/DM and
    # message was sent by the authorised user making the request
    if found_message_id == 1 and found_u_id == 1:
        return True
    
    # If channel_dm_id is odd, this means that message is from channel
    found_owner_creator = 0
    if message_id % 2 == 1:
        for channel in get_data()['channels']:
            if channel['channel_id'] == channel_dm_id:
                for owner in channel['owner_members']:
                    if owner['u_id'] == auth_user_id:
                        found_owner_creator = 1

    # If channel_dm_id is even, this means that message is from DM
    elif message_id % 2 == 0:
        for dm in get_data()['dms']:
            if len(dm['creator']) > 0:
                if dm['creator']['u_id'] == auth_user_id:
                    found_owner_creator = 1

    # In the case where message being edited is part of a channel, 
    # check if auth_user_id is global owner of Streams
    if message_id % 2 == 1:
        if check_permision_id(auth_user_id):
            found_owner_creator = 1

    # Message_id refers to a valid message in joined channel/DM and
    # authorised user has owner permissions in the channel/DM
    if found_message_id == 1 and found_owner_creator == 1:
        return True
    else:
        return False


# Helper function for message_edit
# Returns a dictionary of dm with given dm_id
def get_message_dict(message_id):
    '''
    return type: dictionary
    '''
    for message in get_data()['messages']:
        if message['message_id'] == message_id:
            return message

# Helper function for message_Edit
# Returns true if valid message length
# Returns false otherwise
def check_valid_message_send_format(message):
    len_message = len(message)
    if len_message > 1000:
        return False
    else:
        return True 


#################################################
######## Helper functions for dm.py      ########
#################################################


# Helper function for dm_details, dm_leave, dm_messages, messages_senddm
# Returns true if valid memeber in dm
# Returns false otherwise
def check_valid_member_in_dm(dm_id, auth_user_id):
    '''
    return type: bool
    '''
    for dm in get_data()['dms']:
        if dm['dm_id'] == dm_id:
            for member in dm['members']:
                if member['u_id'] == auth_user_id:
                    return True
    return False


# Helper function for message_senddm
# Returns true if valid message length
# Returns false otherwise
def check_valid_message(message):
    len_message = len(message)
    if len_message > 1000 or len_message < 1:
        return False
    else:
        return True 

# Helper function for dm_create
# Returns handle of user
def get_handle(auth_user_id):
    '''
    return type: <string>
    '''
    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            return user['handle_str']

# Helper function for dm_remove
# Returns true if creator of dm
# Returns false otherwise
def check_creator(auth_user_id):
    '''
    return type: bool
    '''
    for dm in get_data()['dms']:
        if len(dm['creator']) > 0:
            if dm['creator']['u_id'] == auth_user_id:
                return True
    return False

# Helper function for dm_remove, dm_details, dm_leave, dm_messages, message_senddm
# Returns true if dm exists
# Returns false otherwise
def check_valid_dm(dm_id):
    '''
    return type: bool
    '''
    for dm in get_data()['dms']:
        if dm['dm_id'] == dm_id:
            return True
    return False

# Helper function for dm_remove, dm_details, dm_messages, message_send_dm
# Returns a dict of dm if given dm_id exists
def get_dm_dict(dm_id):
    '''
    return type: dictionary
    '''
    for dm in get_data()['dms']:
        if dm['dm_id'] == dm_id:
            return dm
