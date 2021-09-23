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
    from data_store import data_store, initial_object
    listchannel = []
    for channels in initial_object['channels']:
        if channels['auth_user_id'] = auth_user_id;
            listchannel.append(channels)
'channels' = listchannel
    return {
        'channels': [
        	{
        		'channel_id': channels,
        		'name': name,
                'is public': is_public,
                'owner_members': auth_user_id, 
                'all_members': {auth_user_id}
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    return {
        'channel_id': 1,
    }
