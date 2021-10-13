from src.server_helper import decode_token
from src.helper import check_valid_email, channels_user_details
from src.error import InputError
from src.data_store import DATASTORE, initial_object


def dm_details_v1(): 
    '''
    <Brief description of what the function does>

Arguments:
    <name> (<data type>)    - <description>
    <name> (<data type>)    - <description>
    ...

Exceptions:
    InputError  - Occurs when ...
    AccessError - Occurs when ...

Return Value:
    Returns <return value> on <condition>
    Returns <return value> on <condition>
    '''