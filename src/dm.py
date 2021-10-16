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


# for testing

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
    for i in range(len(u_ids)):
        if not channels_create_check_valid_user(u_ids[i]):
            raise InputError('any u_id in u_ids does not refer to a valid user')
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
    member_list = [creator_info]

    for i in range(len(u_ids)):
        handle = get_handle(u_ids[i])
        handle_list.append(handle)
        info = user_info(u_ids[i])
        member_list.append(info)
    # alphabetically-sorted
    handle_list.sort()
    separation = ", "
    name = separation.join(handle_list)

    dm = {
        'dm_id': dm_id,
        'name': name,
        'creator': creator_info,
        'members': member_list
    }
    dms.append(dm)
    DATASTORE.set(store)
    return {
        'dm_id': dm_id
    }

def dm_list_v1(token):
    auth_user_id = decode_token(token)
    return {'dms': get_dm_info(auth_user_id)}

def dm_remove_v1(token, dm_id):    
    # assume type is always correct?
    if not isinstance(dm_id, int):
        raise InputError("This is an invalid dm_id")
    
    if not check_valid_dm(dm_id):
        raise InputError("This does not refer to a valid dm")

    auth_user_id = decode_token(token)
    if not check_creator(auth_user_id, dm_id):
        raise AccessError('The user is not the original DM creator')

    store = DATASTORE.get()
    dms = initial_object['dms']
    dm = get_dm_dict(dm_id)
    dms.remove(dm)
    DATASTORE.set(store)
    return {}

def message_senddm_v1(token, dm_id, message):
    
    auth_user_id = decode_token(token)
    store = DATASTORE.get()

    # Invalid dm_id
    if not check_valid_channel_id(dm_id):
        raise InputError("The dm_id does not refer to a valid dm")

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(dm_id, auth_user_id):
        raise AccessError("Authorised user is not a member of dm with dm_id")

    # Invalid message: Less than 1 or over 1000 characters
    if not check_valid_message(message):
        raise InputError("Message is invalid as length of message is less than 1 or over 1000 characters.")

    # Creating unique message_id 
    dm_id = (len(initial_object['message']) * 2) 

    # Current time message was created and sent
    time_created = time.time()

    dmsend_details = {
        'message_id': message_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created
    }

    # Append dictionary of message details into initial_objects['dm']['messages']
    for dm in initial_object['dm']:
        if dm['dm_id'] == dm_id:
            dm['message'].append(dmsend_details)

    # Append dictionary of message details into intital_objects['messages']
    dmsend_details['dm_id'] = dm_id
    initial_object['dm'].append(dmsend_details)

    DATASTORE.set(store)

    return {
        'message_id': dm_id
    }

'''
id1 = auth_register_v2('abc@gmail.com', 'password', 'leanna', 'chan')
id2 = auth_register_v2('asdsfb@gmail.com', 'password', 'hi', 'wore')
id3 = auth_register_v2('asdsfbdfhdj@gmail.com', 'password', 'hello', 'world')
id4 = auth_register_v2('asbfdhfhrdfhdj@gmail.com', 'password', 'baby', 'shark')
dm1 = dm_create_v1(id1['token'], [id2['auth_user_id'], id3['auth_user_id']])
dm2 = dm_create_v1(id2['token'], [id3['auth_user_id'], id4['auth_user_id'], id1['auth_user_id']])
dm3 = dm_create_v1(id3['token'], [id4['auth_user_id'], id1['auth_user_id']])
dm_remove_v1(id1['token'], dm1['dm_id'])
dm_remove_v1(id3['token'], dm3['dm_id'])
dm_remove_v1(id3['token'], dm2['dm_id'])
#print(dm_list_v1(id3['token']))
'''
