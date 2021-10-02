from src.data_store import data_store, initial_object
from src.error import InputError, AccessError
from src.helper import channels_create_check_valid_user, channels_user_details, user_info

def channels_list_v1(auth_user_id):
    '''
    Provide a list of all channels (and their associated details) 
    that the authorised user is part of.

    Arguments:
        <auth_user_id> (<int>)    - unique id of an authorised user
        ...

    Exceptions:
        AccessError  - Occurs when the auth_user_id input is not a valid type
                     - Occurs when the auth_user_id doesn't refer to a valid user
       
    Return Value:
        Returns <{channels}> when all channels (and its details) that user 
        is part of are successfully listed by authorised user
    '''

    store = data_store.get()

    # Invalid auth_user_id
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth_user_id')
    if not channels_create_check_valid_user(auth_user_id):
        raise AccessError('The auth_user_id does not refer to a valid user')

    new_list = []

    for channel in initial_object['channels']:
        for member in channel['all_members']:
            # if the users are authorised (the auth_user_id can be found in the user list)
            if member['u_id'] == auth_user_id:
                # append to an empty list
                new_list.append({'channel_id' : channel['channel_id'], 'name': channel['name']})   
    
    data_store.set(store)

    # return to the new list    
    return {
        'channels': new_list
    }
    
def channels_listall_v1(auth_user_id):
    '''
    Provide a list of all channels, including private channels, 
    (and their associated details)

    Arguments:
        <auth_user_id> (<int>)    - unique id of an authorised user
        ...

    Exceptions:
        AccessError  - Occurs when the auth_user_id input is not a valid type
                     - Occurs when the auth_user_id doesn't refer to a valid user
       
    Return Value:
        Returns <{channels}> when all channels (and its details) in Streams 
        are successfully listed by authorised user
    '''

    store = data_store.get()

    # Invalid auth_user_id
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth_user_id')
    if not channels_create_check_valid_user(auth_user_id):
        raise AccessError('The auth_user_id does not refer to a valid user')

    listchannel = []
    for channels in initial_object['channels']:
        listchannel.append({'channel_id' : channels['channel_id'], "name": channels['name']})
   
    data_store.set(store)
    return {
        'channels': listchannel
    }

# Creates a new channel with the given name that is either a public or private channel. 
def channels_create_v1(auth_user_id, name, is_public):
    '''  
    Arguments:
        <auth_user_id> (<int>)     - unique id of an authorised user
        <name>         (<string>)  - the name of the channel
        <is_public>    (<boolean>) - privacy setting: True - Public ; False - Private
    
    Exceptions:
        InputError  - Occurs when the length of name is less than 1 or more than 20 characters;
                    - Occurs when then name is blank e.g., ' '

        AccessError - Occurs when the auth_user_id input is not a valid type
                    - Occurs when the auth_user_id doesn't refer to a valid user

    Return Value: 
        Returns <{channel_id}> when the channel is sucessfully created
    '''
    store = data_store.get()

    # Invalid auth_user_id
    if not isinstance(auth_user_id, int):
        raise AccessError('This is an invalid auth_user_id')
    if not channels_create_check_valid_user(auth_user_id):
        raise AccessError('The auth_user_id does not refer to a valid user')

    # Invalid channel name
    if len(name) not in range(1, 21):
        raise InputError('Length of name is less than 1 or more than 20 characters')
    if name[0] == ' ':
        raise InputError('Name cannot be blank')

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
