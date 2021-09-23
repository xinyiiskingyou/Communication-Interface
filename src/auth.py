from src.data_store import data_store, initial_object
from src.error import InputError

def auth_login_v1(email, password):
    store = data_store.get()
    
    for user in initial_object['users']:
        if (user['email'] == email) & (user['password'] == password):
            return user['auth_user_id']
        else:
            raise InputError("Email and/or password is not valid!")



def auth_register_v1(email, password, name_first, name_last):
    return {
        'auth_user_id': 1,
    }
