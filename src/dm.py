from src.server_helper import decode_token
from src.error import InputError
from src.helper import channels_create_check_valid_user, get_handle, get_dm_info, user_info
from src.data_store import DATASTORE, initial_object

# for testing
from src.auth import auth_register_v2
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
    pass

'''
id1 = auth_register_v2('abc@gmail.com', 'password', 'leanna', 'chan')
id2 = auth_register_v2('asdsfb@gmail.com', 'password', 'hi', 'wore')
id3 = auth_register_v2('asdsfbdfhdj@gmail.com', 'password', 'hello', 'world')
id4 = auth_register_v2('asbfdhfhrdfhdj@gmail.com', 'password', 'baby', 'shark')
token = id1['token']
dm_create_v1(token, [id2['auth_user_id'], id3['auth_user_id']])
dm_create_v1(id2['token'], [id3['auth_user_id'], id4['auth_user_id'], id1['auth_user_id']])
dm_create_v1(id3['token'], [id4['auth_user_id'], id1['auth_user_id']])
print(dm_list_v1(id3['token']))
'''