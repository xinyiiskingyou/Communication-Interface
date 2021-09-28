from src.data_store import data_store, initial_object 
from src.auth import auth_register_v1
from src.error import InputError, AccessError
from channels import channels_create_check_valid_user


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    '''
    raise error :
    input  
    - channel id not valid/doesn't have a valid channel 
    - authoried user is alreadt a member of the channel 
    access
    - when a channel is private and authorised user is not a member - also not global owner 

    to do: 
    take in an authuserid and channel id and append them to the member list in channels dictionary 
    ''' 
    if channels_create_check_valid_user(auth_user_id) == False:
        raise AccessError ('Auth_user_id is not a valid id')
    if 



    return {
    }
