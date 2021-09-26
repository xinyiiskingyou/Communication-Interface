from src.data_store import data_store, initial_object
from src.error import InputError
from src.auth import auth_register_v1
def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

# Creates a new channel with the given name that is either a public or private channel. 
def channels_create_v1(auth_user_id, name, is_public):
    '''    
    return type: dict contains type 'channels_id' 
    '''
    
    # error handling
    if len(name) not in range(1, 21):
        raise InputError('length of name is less than 1 or more than 20 characters')
    if name[0] == ' ':
        raise InputError('name cannot be blank')
    if is_public not in range(0,2):
        raise InputError('the channel has to be either public or private')
    if not isinstance(auth_user_id, int):
        raise InputError('this is an invalid auth user id')
    if not channels_create_check_valid_user(auth_user_id):
        raise InputError('this is an invalid auth user id')

    channels = initial_object['channels']
    channel_id = len(channels) + 1
    owner = (channels_user_details(auth_user_id))
    new = {'channel_id': channel_id, 'name': name, 'is_public': is_public, 'owner_members': owner, 'all_members': owner}
    channels.append(new)
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



