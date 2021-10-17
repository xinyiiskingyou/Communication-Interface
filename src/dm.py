from src.server_helper import decode_token
from src.helper import check_valid_email, channels_user_details, check_valid_dm, check_valid_member_in_dm, channels_create_check_valid_user, get_handle, get_dm_info, user_info, check_creator, check_valid_dm, get_dm_dict
from src.error import InputError, AccessError
from src.data_store import DATASTORE, initial_object
from src.auth import auth_register_v2

def dm_details_v1(token, dm_id): 
    '''
    Given an dm_id and token, the function provides
    basic details about the dm 

Arguments:
    token ()    - a user's unique token 
    dm_id (int) - a user's unique dm id 
    ...

Exceptions:
    InputError  - Occurs when the dm id is invalid 
                    or the token is invalid.
    AccessError - Occurs when the dm_id is not 
                    an authorised member of the DM 

Return Value:
    Returns name 
    Returns members
    '''
    # store = DATASTORE.get() 
    auth_user_id = decode_token(token)



    if not check_valid_dm(dm_id): 
        raise InputError("This dm_id does not refer to a valid DM")

    #not a valid user 
    if not check_valid_member_in_dm(dm_id, auth_user_id): 
        raise AccessError("The user is not an authorised member of the DM")

    for dm in initial_object['dms']: 
        if dm_id == dm['dm_id']: 
            return { 
                'name': dm['name'],
                'members': dm['members']
            }


# def dm_messages_v1(): 
#     '''
#     Given a dm with dm_id that authorised user
#     is a member, return up to 50 messages between a index "start"
#      and "start + 50". Message with index 0 is the most recent message 
#     in the channel. returns a new index 'end'  which is 'start + 50'. 
#     returns -1 in end - no more messages to load. 

# Arguments: 
#     token - a user's unique token 
#     dm_id (int) - a user's unique dm id
#     start -  
#     ...

# Exceptions:
#     InputError  - Occurs when the dm id is invalid 
#                     or the token is invalid.
#                 - Start is greater then total number
#                 of messages in channel 
#     AccessError - Occurs when the dm_id is not 
#                     an authorised member of the DM 

# Return Value:
#     Returns end 
#     '''

#     #invalid dm_id
#     if not check_valid_dm_id(dm_id): 
#         raise InputError("This dm_id does not refer to a valid DM")

#     #not authorised  
#     if not check_valid_member_in_dm(dm_id, auth_user_id): 
#         raise AccessError("The user is not an authorised member of the DM")



# create a dm and returns it id
def dm_create_v1(token, u_ids):
    '''
    Creates a dm with name generated based on users' handle

    Arguments:
        <token>        (<hash>)    - an authorisation hash
        <u_ids>        (<list>)    - a list of u_id 

    Exceptions:
        InputError  - Occurs when one of u_id given does not refer to a valid user

    Return Value:
        Returns <{dm_id}> when the dm is sucessfully created
    '''

    # error handling
    for i in range(len(u_ids)):
        if not channels_create_check_valid_user(u_ids[i]):
            raise InputError(description = 'any u_id in u_ids does not refer to a valid user')

    store = DATASTORE.get()
    auth_user_id = decode_token(token)

    dms = initial_object['dms']
    # generate dm_id according the number of existing dms
    dm_id = len(dms) + 1

    # create a list that stores the handles of all the users given 
    # including creator
    handle_list = []
    creator_handle = get_handle(auth_user_id)
    handle_list.append(creator_handle)
    creator_info = user_info(auth_user_id)

    # create a list that stores member's info
    member_list = [creator_info]

    for i in range(len(u_ids)):
        handle = get_handle(u_ids[i])
        handle_list.append(handle)
        info = user_info(u_ids[i])
        member_list.append(info)

    # alphabetically-sorted the handle
    handle_list.sort()

    # generate a name that consist of all 
    # members handle and separated by comma
    separation = ", "
    name = separation.join(handle_list)

    dm = {
        'dm_id': dm_id,
        'name': name,
        'creator': creator_info,
        'members': member_list,
        'messages': []
    }
    dms.append(dm)
    DATASTORE.set(store)
    return {
        'dm_id': dm_id
    }

# get the list of dm that the user is a member of
def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of.

    Arguments:
        <token>        (<hash>)    - an authorisation hash

    Exceptions:
        N/A

    Return Value:
        Returns <{'dms'}> where 'dms' is a list of dictionary of dm 
        that this user is a member of
    '''
    auth_user_id = decode_token(token)
    return {'dms': get_dm_info(auth_user_id)}

def dm_remove_v1(token, dm_id):    
    '''
    Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.

    Arguments:
        <token>        (<hash>)    - an authorisation hash
        <dm_id>        (<int>)     - an unique id of a dm
    Exceptions:
        Input Error    - when dm_id does not refer to a valid DM
        Access Error   - when dm_id is valid and the auth user is not
                         original DM creator. 

    Return Value:
        Returns N/A
    '''
    if not isinstance(dm_id, int):
        raise InputError(description = "This is an invalid dm_id")
    
    if not check_valid_dm(dm_id):
        raise InputError(description = "This does not refer to a valid dm")

    auth_user_id = decode_token(token)
    if not check_creator(auth_user_id, dm_id):
        raise AccessError(description = 'The user is not the original DM creator')

    store = DATASTORE.get()
    dms = initial_object['dms']
    dm = get_dm_dict(dm_id)
    dms.remove(dm)
    DATASTORE.set(store)
    return {}

