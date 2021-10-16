from src.server_helper import decode_token
from src.error import InputError, AccessError
from src.helper import channels_create_check_valid_user, get_handle, get_dm_info, user_info, check_creator, check_valid_dm, get_dm_dict
from src.data_store import DATASTORE, initial_object

# create a dm and returns it id
def dm_create_v1(token, u_ids):
    '''
    Creates a dm with name generated based on users' handle

    Arguments:
        <token>        (<string>)    - an authorisation hash
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
    member_list = []
    creator_handle = get_handle(auth_user_id)
    handle_list.append(creator_handle)
    creator_info = user_info(auth_user_id)

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
