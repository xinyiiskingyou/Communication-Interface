from data_store import data_store

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
    '''

    '''
    parameter {auth_user_id, name, is_public}
    return type {channel_id}
    suffix id = integer
    name = strings
    is_public = bool
    
    store = data_store.get()
    channels = store['channels']
    channels.append('CAMEL')
    print(store)
    '''
    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }
    # 目前只有users才能用，想如何建立多一個channel
    names = store['users']
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    print('hi')
    return {
        'channel_id': 1,
    }
channels_create_v1(1,'CAMEL',1)