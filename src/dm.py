from src.server_helper import decode_token, valid_user
from src.helper import channels_create_check_valid_user, get_handle, user_info, check_creator, check_valid_dm, get_dm_dict, check_valid_start
from src.helper import check_valid_member_in_dm, check_valid_message
from src.server_helper import decode_token, valid_user
from src.error import InputError, AccessError
from src.data_store import get_data, save
import time

def dm_create_v1(token, u_ids):
    '''
    Creates a dm with name generated based on users' handle

    Arguments:
        <token>        (<string>)    - an authorisation hash
        <u_ids>        (<list>)      - a list of u_ids

    Exceptions:
        InputError  - Occurs when one of u_id given does not refer to a valid user
        AccessError - Occurs when token is invalid

    Return Value:
        Returns <{dm_id}> when the dm is sucessfully created
    '''

    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # error handling
    for i in range(len(u_ids)):
        if not channels_create_check_valid_user(u_ids[i]):
            raise InputError(description= 'any u_id in u_ids does not refer to a valid user')

    complete_dms = get_data()['dms']
    # generate dm_id according the number of existing dms
    dm_id = len(complete_dms) + 1

    # create a list that stores the handles of all the users given 
    # including creator
    handle_list = []
    creator_handle = get_handle(auth_user_id)
    handle_list.append(creator_handle)
    creator_info = user_info(auth_user_id)

    # create a list that stores member's info
    member_list = [creator_info]

    for i in range(len(u_ids)):
        # append the handle of the users
        handle = get_handle(u_ids[i])
        handle_list.append(handle)

        # append the info of the users
        info = user_info(u_ids[i])
        member_list.append(info)

    # alphabetically-sorted the handle
    handle_list.sort()

    # generate a name that consist of all 
    # members handle and separated by comma
    separation = ", "
    name = separation.join(handle_list)

    get_data()['dms'].append({
        'dm_id': dm_id,
        'name': name,
        'creator': creator_info,
        'members': member_list,
        'messages': [],
    })

    save()
    return {
        'dm_id': dm_id
    }

def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of.

    Arguments:
        <token>        (<string>)    - an authorisation hash

    Exceptions:
        AccessError - Occurs when token is invalid

    Return Value:
        Returns <{'dms'}> where 'dms' is a list of dictionary of dm that this user is a member of
    '''
    #not valid 
    if not valid_user(token):
        raise AccessError(description='User is not valid')
    #creating the list 
    auth_user_id = decode_token(token)
    dm_list = []
    for dm in get_data()['dms']:
        for member in dm['members']:
            if member['u_id'] == auth_user_id:
                dm_list.append({'dm_id': dm['dm_id'], 'name': dm['name']})

    return {'dms':dm_list}

def dm_remove_v1(token, dm_id):    
    '''
    Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Arguments:
        <token>        (<strinf>)    - an authorisation hash
        <dm_id>        (<int>)     - an unique id of a dm

    Exceptions:
        Input Error     - when dm_id does not refer to a valid DM
        AccessError     - when dm_id is valid and the auth user is not original DM creator. 
                        - Occurs when token is invalid

    Return Value:
        Returns N/A
    '''
    #not valid 
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # invalid dm_id
    if not check_valid_dm(dm_id):
        raise InputError(description= "This does not refer to a valid dm")

    # valid dm_id but user is not the dm creator
    if not check_creator(auth_user_id):
        raise AccessError(description= 'The user is not the original DM creator')

    dms = get_data()['dms']
    for dm in dms:
        if dm['dm_id'] == dm_id:
            dms.remove(dm)
            save()

    return {}

def dm_details_v1(token, dm_id): 
    '''
    Given an dm_id and token, the function provides basic details about the dm 

    Arguments:
        token   (<string>)        - a user's unique token 
        dm_id   (<int>)           - a user's unique dm id 
        ...

    Exceptions:
        InputError  - Occurs when the dm id is invalid 
        AccessError - Occurs when the dm_id is not an authorised member of the DM 
                    - Occurs when the token is invalid.

    Return Value:
        Returns name 
        Returns members
    '''
    #not valid 
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    #not valid dm 
    if not check_valid_dm(dm_id): 
        raise InputError(description="This dm_id does not refer to a valid DM")

    # not a valid user 
    if not check_valid_member_in_dm(dm_id, auth_user_id): 
        raise AccessError(description="The user is not an authorised member of the DM")

    dm = get_dm_dict(dm_id)
    return { 
        'name': dm['name'],
        'members': dm['members']
    }

def dm_leave_v1(token, dm_id):
    '''
    Given a DM ID, the user is removed as a member of this DM.

    Arguments:
        <token>        (<hash>)    - an authorisation hash
        <u_ids>        (<list>)    - a list of u_id 

    Exceptions:
        InputError  - Occurs when one of u_id given does not refer to a valid user

        AccessError - Occurs when the token is invalid.
                    - dm_id is valid and the authorised user is not a member of the DM

    Return Value:
        Returns <{dm_id}> when the dm is sucessfully created
    '''
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)
    newuser = user_info(auth_user_id)
    
    # dm_id does not refer to a valid DM
    if not isinstance(dm_id, int):
        raise InputError(description="This is an invalid dm_id")
    if not check_valid_dm(dm_id):
        raise InputError(description="This does not refer to a valid dm")

    # dm_id is valid and the authorised user is not a member of the DM
    if not check_valid_member_in_dm(dm_id, auth_user_id): 
        raise AccessError(description="The user is not an authorised member of the DM")

    for dm in get_data()['dms']: 
        if dm['dm_id'] == dm_id:
            for member in dm['members']:
                if member['u_id'] == auth_user_id: 
                    dm['members'].remove(newuser)
            #clearing the creator if the creator leaves 
            if len(dm['creator']) > 0:
                if dm['creator']['u_id'] == auth_user_id:
                    dm['creator'].clear()
        save()
    save()
    return{}

def dm_messages_v1(token, dm_id, start): 
    '''
    Given a dm with dm_id that authorised user
    is a member, return up to 50 messages between a index "start"
    and "start + 50". Message with index 0 is the most recent message 
    in the channel. returns a new index 'end'  which is 'start + 50'. 
    returns -1 in end - no more messages to load. 

    Arguments: 
        token   (<string>)  - a user's unique token 
        dm_id   (<int>)     - a user's unique dm id
        start   (<int>)     - starting index of message pagination
        ...

    Exceptions:
        InputError  - Occurs when the dm id is invalid or the token is invalid.
                    - Start is greater then total number of messages in channel 
        AccessError - Occurs when the dm_id is not an authorised member of the DM 
                    - Occurs when invalid token

    Return Value:
        Returns end - if end is -1 then it returns the recent messages of the channel 
    '''
    #not valid 
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # invalid dm_id
    if not check_valid_dm(dm_id): 
        raise InputError(description="This dm_id does not refer to a valid DM")

    # not authorised  
    if not check_valid_member_in_dm(dm_id, auth_user_id): 
        raise AccessError(description="The user is not an authorised member of the DM")

    dm = get_dm_dict(dm_id)
    num_messages = len(dm['messages'])
    dm_pagination = dm['messages']

    end = start + 50 
    if end >= num_messages: 
        end = -1

    # Start is greater than the total number of messages in the channel
    if not check_valid_start(num_messages, start): 
        raise InputError(description = 'Start is greater then total messages')
    #PAGINATION 
    if end == -1: 
        dm_pagination = dm_pagination[start:] 
    else: 
        dm_pagination = dm_pagination[start:end]

    return { 
        'messages': dm_pagination,
        'start': start,
        'end': end,
    }

def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id. 

    Arguments: 
        token   (<string>)  - a user's unique token 
        dm_id   (<int>)     - a user's unique dm id
        message (<string>)  - the content of the message

    Exceptions:
        InputError  - Occurs when dm_id does not refer to a valid DM.
                    - Occurs when length of message is less than 1 or over 1000 characters
        AccessError - Occurs when the dm_id is valid and the authorised user is not a member of the DM
                    - Occurs when invalid token

    Return Value:
        Returns end - if end is -1 then it returns the recent messages of the channel 
    '''
    
    if not valid_user(token):
        raise AccessError(description='User is not valid')

    auth_user_id = decode_token(token)

    # Invalid dm_id
    if not check_valid_dm(dm_id):
        raise InputError(description="The dm_id does not refer to a valid dm")

    # Authorised user not a member of channel
    if not check_valid_member_in_dm(dm_id, auth_user_id):
        raise AccessError(description="Authorised user is not a member of dm with dm_id")

    # Invalid message: Less than 1 or over 1000 characters
    if not check_valid_message(message):
        raise InputError(description="Message is invalid as length of message is less than 1 or over 1000 characters.")

    # Creating unique message_id 
    dmsend_id = (len(get_data()['messages']) * 2) 

    # Current time message was created and sent
    time_created = int(time.time())

    dmsend_details_dm = {
        'message_id': dmsend_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created
    }

    # Append dictionary of message details into initial_objects['dm']['messages']
    for dm in get_data()['dms']:
        if dm['dm_id'] == dm_id:
            dm['messages'].insert(0, dmsend_details_dm)
            save()

    dmsend_details_messages = {
        'message_id': dmsend_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created, 
        'dm_id': dm_id
    }

    # Append dictionary of message details into intital_objects['messages']
    get_data()['messages'].insert(0, dmsend_details_messages)
    save()

    return {
        'message_id': dmsend_id
    }
