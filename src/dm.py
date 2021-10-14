from src.server_helper import decode_token
from src.helper import check_valid_email, channels_user_details, check_valid_dm_id, check_valid_member_in_dm
from src.error import InputError
from src.data_store import DATASTORE, initial_object


def dm_details_v1(): 
    '''
    Given an dm_id and token, the function provides
    basic details about the dm 

Arguments:
    token ()    - a user's unique token 
    dm_id (int) - a user's unique dm id 
    ...

Exceptions:
    InputError  - Occurs when the dm id is invalid 
                    or the token is invalid.
    AccessError - Occurs when the dm_id is not 
                    an authorised member of the DM 

Return Value:
    Returns name 
    Returns members
    '''
    store = DATASTORE.get() 
    auth_user_id = decode_token(token)
    
    if not check_valid_dm_id(dm_id): 
        raise InputError("This dm_id does not refer to a valid DM")

    #not a valid user 
    if not check_valid_member_in_dm(dm_id, auth_user_id): 
        raise AccessError("The user is not an authorised member of the DM)

    for dms in initial_object['dms']: 
        if dm_id == dms['dm_id']: 
            return { 
                'name': dms['name']
                'members': dms['members']
            }


def dm_messages_v1(): 
    '''
    Given a dm with dm_id that authorised user
    is a member, return up to 50 messages between a index "start"
     and "start + 50". Message with index 0 is the most recent message 
    in the channel. returns a new index 'end'  which is 'start + 50'. 
    returns -1 in end - no more messages to load. 

Arguments:
    token - a user's unique token 
    dm_id (int) - a user's unique dm id
    start -  
    ...

Exceptions:
    InputError  - Occurs when the dm id is invalid 
                    or the token is invalid.
                - Start is greater then total number
                of messages in channel 
    AccessError - Occurs when the dm_id is not 
                    an authorised member of the DM 

Return Value:
    Returns end 
    '''

    #invalid dm_id
    if not check_valid_dm_id(dm_id): 
        raise InputError("This dm_id does not refer to a valid DM")

    #not authorised  
    if not check_valid_member_in_dm(dm_id, auth_user_id): 
        raise AccessError("The user is not an authorised member of the DM)

    