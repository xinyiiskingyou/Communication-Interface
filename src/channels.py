from src.data_store import data_store, initial_object
from src.error import InputError

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
    '''
    Provides a list of all channels, including private channels (and their associated 
    details)

    auth_user_id is the name of the user we connecting from 
    '''

    listchannel = []
    for channels in initial_object['channels']:
        if channels['auth_user_id'] == auth_user_id:
            listchannel.append({'channel_id' : channel['channel_id'], name: channel['name']})
    return {'channels': listchannel}
        # 'channels': [
        # 	{
        # 		'channel_id': channels,
        # 		'name': name,
        #         'is public': is_public,
        #         'owner_members': auth_user_id, 
        #         'all_members': {auth_user_id}
        # 	}
        # ],

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Creates a new channel with the given name that is either a public or private channel. 
    The user who created it automatically joins the channel. 
    For this iteration, the only channel owner is the user who created the channel.
    
    parameter {auth_user_id, name, is_public}
    return type {channel_id}
    suffix id = integer
    name = strings
    is_public = bool

    channels = List of dictionaries, where each dictionary contains types { channel_id, name }
    '''
    ## to do:
    # channel name cannot be duplicate

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
    new = {'channel_id': channel_id, 'name': name, 'is_public': is_public, 'owner_members': auth_user_id, 'all_members': {auth_user_id}}
    channels.append(new)

    return {
        'channel_id': channel_id,
    }

def channels_create_check_valid_user(auth_user_id):
    '''
    return type: bool
    '''
    for user in initial_object['users']:
        if user['auth_user_id'] == auth_user_id:
            return True
    return False

# print(channels_create_v1(1,'CAMEL',0))
# print(channels_create_v1(2,'1531',1))

