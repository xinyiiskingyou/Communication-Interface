from src.data_store import data_store, initial_object
from src.error import InputError

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
    for channel in initial_object['channels']:
        for member in channel['all_members']:
            for user in initial_object['users']:
                if member['u_id'] == user['auth_user_id']:
                    new_list.append({'channel_id' : channel['channel_id'],
                    'name': channel['name']})
                
    return {'channels': new_list}


def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):

    if len(name) not in range(1, 21):
        raise InputError('length of name is less than 1 or more than 20 characters')
    if name[0] == ' ':
        raise InputError('name cannot be blank')
    if is_public not in range(0,2):
        raise InputError('the channel has to be either public or private')
    if not isinstance(auth_user_id,int):
        raise InputError('this is an invalid auth user id')

    store = data_store.get()
    channels = initial_object['channels']
    channel_id = len(channels) + 1
    new = {
        'channel_id': channel_id, 
        'name': name, 
        'is_public': bool(is_public), 
        'owner_members': [],
        'all_members': []
    }
    
    new['all_members'].append({'u_id': auth_user_id})
    #print('number of channels', channel_id)
    initial_object['channels'].append(new)
    data_store.set(store)
    return {
        'channel_id': new['channel_id']
    }


def channels_create_check_valid_user(auth_user_id):
    '''
    return type: bool
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return True
    return False

