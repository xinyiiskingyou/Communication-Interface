'''
Notifications implementation
'''

from src.data_store import get_data, save
from src.error import InputError, AccessError
from src.server_helper import decode_token, valid_user

def notifications_get_v1(token):
    pass