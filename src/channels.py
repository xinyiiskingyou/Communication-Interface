from src.data_store import data_store, initial_object
from src.error import InputError, AccessError

def channels_list_v2(auth_user_id):
    '''
    Provide a list of all channels (and their associated details) 
    that the authorised user is part of.

    Arguments:
        auth_user_id
    Return Value:
        returns channel_id and name if an authorised user has channel
    '''
    # for all channels
    # -> if the users are authorised
    # -> append to an empty list
    # return to the new list

    new_list = []

    for channels in initial_object['channels']:
        for member in channels['all_members']:
            for user in initial_object['users']:
                if member['auth_user_id'] == user['auth_user_id']:
                    new_list.append({'channel_id' : channels['channel_id'],
                    'name': channels['name']})       
    return {'channels': new_list}
    
def channels_listall_v1(auth_user_id):
    '''
    Provides a list of all channels, including private channels (and their associated 
    details)

    auth_user_id is the name of the user we connecting from 
    '''

    listchannel = []
    for channels in initial_object['channels']:
        listchannel.append({'channel_id' : channels['channel_id'], "name": channels['name']})
    return {'channels': listchannel}

# Creates a new channel with the given name that is either a public or private channel. 
def channels_create_v1(auth_user_id, name, is_public):
    '''    
    return type: dict contains type 'channels_id' 
    '''
    store = data_store.get()
    # error handling
    if len(name) not in range(1, 21):
        raise InputError('length of name is less than 1 or more than 20 characters')
    if name[0] == ' ':
        raise InputError('name cannot be blank')
    if is_public not in range(0,2):
        raise InputError('the channel has to be either public or private')
    if not isinstance(auth_user_id, int):
        raise AccessError('this is an invalid auth user id')
    if not channels_create_check_valid_user(auth_user_id):
        raise AccessError('this is an invalid auth user id')

    channels = initial_object['channels']
    # generate channel_id according the number of existing channels
    channel_id = len(channels) + 1
    owner = (channels_user_details(auth_user_id))
    new = {'channel_id': channel_id, 'name': name, 'is_public': is_public, 'owner_members': [owner], 'all_members': [owner]}
    channels.append(new)
    data_store.set(store)

    return channel_id

# helper function to check if the auth_user_id given is registered
def channels_create_check_valid_user(auth_user_id):
    '''
    return type: bool
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return True
    return False

# helper function to access to details of the given auth_user_id
def channels_user_details(auth_user_id):
    '''
    return type: dict
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return user
    return {}

