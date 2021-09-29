from data_store import data_store, initial_object
from error import InputError, AccessError

def channels_list_v2(auth_user_id):
    '''
    Provide a list of all channels (and their associated details) 
    that the authorised user is part of.

    Arguments:
        auth_user_id
    Return Value:
        returns channel_id and name if an authorised user has channel
    '''
    new_list = []

    for channel in initial_object['channels']:
        for member in channel['all_members']:
            for user in initial_object['users']:
                # if the users are authorised (the auth_user_id can be found in the user list)
                if member['auth_user_id'] == user['auth_user_id']:
                    # append to an empty list
                    new_list.append({'channel_id' : channel['channel_id'],
                    'name': channel['name']})   
    # return to the new list    
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

    user = user_info(auth_user_id)
    new = {
        'channel_id': channel_id, 
        'name': name, 
        'is_public': bool(is_public), 
        'owner_members': [user],  
        'all_members': [user]
    }

    channels.append(new)
    data_store.set(store)

    return {
        'channel_id': channel_id,
    }

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

def user_info(auth_user_id):
    user = channels_user_details(auth_user_id)
    return {
        'auth_user_id': user['auth_user_id'], 
        'email': user['email'], 
        'name_first': user['name_first'], 
        'name_last': user['name_last'], 
        'handle_str': user['handle_str']
    }