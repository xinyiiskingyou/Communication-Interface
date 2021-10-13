from src.server_helper import decode_token
from src.helper import check_valid_email, channels_user_details
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
    
    #not a valid user 
    if not channels_create_check_valid_user(auth_user_id) 