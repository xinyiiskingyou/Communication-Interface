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
    channel = get_channel_details(channel_id)
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
    channel = get_channel_details(channel_id)
    if not channel['is_public']:
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
    user = get_user_details(auth_user_id)
    # If the user is a global owner
    if user['permission_id'] == 1:
        return True
    return False

# Helper function for channel_join
# Check if the user is an owner of the channel
# Returns true if owner
# Returns false otherwise
def check_valid_owner(auth_user_id, channel_id):
    channel = get_channel_details(channel_id)
    for member in channel['owner_members']:
        if member['u_id'] == auth_user_id:
            return True
    return False

# Helper function for channel_addowner, channel_removeowner
# Checks if auth_user_id has owner permission
# Returns true if they are global owners
# Returns false otherwise
def check_channel_owner_permission(auth_user_id, channel_id):
    found_permission = 0

    channel = get_channel_details(channel_id)
    for member in channel['all_members']:
        if member['u_id'] == auth_user_id:
            if check_permision_id(member['u_id']):
                found_permission = 1
    if check_valid_owner(auth_user_id, channel_id):
        found_permission = 1

    if found_permission == 1:
        return True
    return False

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

# Helper function for message_edit_v1, message_share_v1
# Checks if message_id refers to a valid message within a channel/DM
# that the authorised user has joined
# Returns true if valid message_id
# Returns false otherwise
def check_valid_message_id(auth_user_id, message_id):
    found_message_id = 0
    channel_dm_id = 0

    # Finds whether or not the message_id exists as a valid message
    if not check_valid_channel_dm_message_ids(message_id):
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
        if check_valid_member_in_channel(channel_dm_id, auth_user_id):
            found_user = 1

    # If message_id is odd, message is from DM
    # Go through DMs to determine if user is part of DM of that message_id
    elif message_id % 2 == 0:
        if check_valid_member_in_dm(channel_dm_id, auth_user_id):
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
        if check_valid_owner(auth_user_id, channel_dm_id):
            found_owner_creator = 1

    # If channel_dm_id is even, this means that message is from DM
    elif message_id % 2 == 0:
        if check_creator(auth_user_id):
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
# Returns true if valid message length
# Returns false otherwise
def check_valid_message_send_format(message):
    len_message = len(message)
    if len_message > 1000:
        return False
    else:
        return True 

# Helper function for message/react, message/unreact, message/pin
# Returns true if message_id is valid in channel/dm
# Returns false otherwise
def check_valid_channel_dm_message_ids(message_id):
    
    found = 0
    for channel in get_data()['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                found = 1

    for dm in get_data()['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                found = 1

    if found == 1:
        return True
    return False

# Helper function for message_pin
# Returns true if the user has owner permission
def check_authorised_user_pin(message_id, auth_user_id):
    found = 0
    if message_id % 2 == 1:
        for channel in get_data()['channels']:
            for owner in channel['owner_members']:
                if owner['u_id'] == auth_user_id:
                    found = 1
            for member in channel['all_members']:         
                if member['u_id'] == auth_user_id:
                    if check_permision_id(member['u_id']):
                        found = 1
    if message_id % 2 == 0:
        if check_creator(auth_user_id):
            found = 1
    if found == 1:
        return True
    return False

# Helper function for message/pin, message/react and message/unreact
# Returns a dict of message in the channel or dm 
def get_message(message_id):
    if message_id % 2 == 1:
        for channel in get_data()['channels']:
            for message in channel['messages']:
                if message['message_id'] == int(message_id):
                    return message
    for dm in get_data()['dms']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                return message

# Helper function for message/react and message/unreact
# Returns a dict of react in the channel/dm
def get_reacts(message_id, react_id):
    message = get_message(message_id)
    for react in message['reacts']:
        if react['react_id'] == react_id:
            return react

# Helper function for message_share
# Checks both channel_id and dm_id are valid 
# Return true if both are valid and false otherwise
def check_valid_channel_id_and_dm_id_format(channel_id, dm_id):
    found_channel = 0
    found_dm = 0

    if check_valid_channel_id(channel_id):
        found_channel = 1

    if check_valid_dm(dm_id):
        found_dm = 1

    if ((found_channel == 1 and dm_id == -1) or 
    (channel_id == -1 and found_dm == 1)):
        return True
    else:
        return False
    
# Helper function for message_share
# Checks that authorised user is member of channel/DM they are 
# trying to share the message to
def check_share_message_authorised_user(auth_user_id, channel_id, dm_id):
    if channel_id != -1:
        if check_valid_member_in_channel(channel_id, auth_user_id):
            return True

    if dm_id != -1:
        if check_valid_member_in_dm(dm_id, auth_user_id):
            return True
    
    return False

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
    dm = get_dm_dict(dm_id)
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

# Helper function for dm_create, notification
# Returns handle of user
def get_handle(auth_user_id):
    '''
    return type: <string>
    '''
    user = get_user_details(auth_user_id)
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

# Helper function for dm_remove, dm_details, dm_leave, dm_messages, message_senddm, message_sendlaterdm
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

######################################################
####### Helper functions for notifications.py ########
######################################################

# Helper function in message_send_v1 
# Checks if a member of channel has been tagged
# Return a list of all the handle strings tagged 
# and an empty string if no users are tagged in message
def check_message_channel_tag(message, channel_id):
    handle_str_list = []
    alpha_numeric_str = re.sub("[^0-9a-zA-Z@]+", " ", message)
    for word in alpha_numeric_str.split():
        if '@' in word:
            handle_str = word[1:]
            # print(handle_str)
            channel = get_channel_details(channel_id)
            for member in channel['all_members']:
                # print(f"member = {member}")
                if member['handle_str'] == handle_str:
                    handle_str_list.append(handle_str)
    # print(f"handle_str_list before {handle_str_list}")                     
    # print(f"handle_str_list after {list(set(handle_str_list))}")
    return list(set(handle_str_list))

# Helper function in message_senddm_v1
# Checks if a member of DM has been tagged
# Return true if valid member has been tagged, false otherwise
def check_message_dm_tag(message, dm_id):
    handle_str_list = []
    alpha_numeric_str = re.sub("[^0-9a-zA-Z@]+", " ", message)
    for word in alpha_numeric_str.split():
        if '@' in word:
            handle_str = word[1:]
            dm = get_dm_dict(dm_id)
            for member in dm['members']:
                # print(f"member = {member}")
                if member['handle_str'] == handle_str:
                    handle_str_list.append(handle_str)
    # print(f"handle_str_list before {handle_str_list}")                     
    # print(f"handle_str_list after {list(set(handle_str_list))}")
    return list(set(handle_str_list))

# Helper function in message_react_v1
# Returns the channel_id of message and u_id of user that sent message as a dict
def channel_dm_of_message_id(message_id):
    if message_id % 2 == 1:
        for channel in get_data()['channels']:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    return {
                        'channel_dm_id': channel['channel_id'],
                        'u_id': message['u_id'], 
                    }

    elif message_id % 2 == 0:
        for dm in get_data()['dms']:
            for message in dm['messages']:
                if message['message_id'] == message_id:
                    return {
                        'channel_dm_id': dm['dm_id'],
                        'u_id': message['u_id'],
                    }

# Helper function for activate_notification_tag_channel
# Finds the name of the channel from channel_id
def channel_id_to_channel_name(channel_id):
    channel = get_channel_details(channel_id)
    return channel['name']

# Helper function for activate_notification_tag_dm
# Finds the name of the DM from dm_id
def dm_id_to_dm_name(dm_id):
    dm = get_dm_dict(dm_id)
    return dm['name']
