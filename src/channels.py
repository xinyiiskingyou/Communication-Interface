from data_store import data_store
from error import InputError

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
    # check if the user id exist (is a valid user)
    # channel name cannot be duplicate
    # error handling
    if len(name) < 1 or len(name) > 20:
        raise InputError('length of name is less than 1 or more than 20 characters')
    if name[0] == ' ':
        raise InputError('name cannot be blank')
    store = data_store.get()
    channels = store['channels']
    channel_id = len(channels) + 1
    new = {'channel_id': channel_id, 'name': name}
    
    #print('number of channels', channel_id)
    channels.append(new)
    #print(store)
    return {
        'channel_id': channel_id,
    }
print(channels_create_v1(1,'CAMEL',1))
print(channels_create_v1(2,'CAMEL',1))
print(channels_create_v1(2,'1531',1))
print(channels_create_v1(2,'  ',1))