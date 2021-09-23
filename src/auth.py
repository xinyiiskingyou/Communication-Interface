from src.data_store import data_store, initial_object
from src.error import InputError
import re

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()

    # Creating the basic dictionary to be put into the initial_objects list
    dict_user = {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    }   

    # Error handling
    token = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if not (re.search(token, email)):
        raise InputError("This email is of invalid form")

    # If list is empty add new user info (dict) into initial_objects list
    # else check for duplicates
    if len(initial_object['users']) == 0:
        initial_object['users'].append(dict_user)
    else:
        for user in initial_object['users']:
            if user['email'] == email:
                raise InputError("This email address has already been registered by another user") 

    if len(password) < 6:
         raise InputError("This password is less then 6 characters in length")

    if len(name_first) not in range(1, 51):
         raise InputError("name_first is not between 1 - 50 characters in length")

    if len(name_last) not in range(1, 51):
         raise InputError("name_last is not between 1 - 50 characters in length")
         
    # Creating unique user_id and adding to dict_user
    user_id = len(initial_object['users'])
    dict_user[user_id] = user_id

    # Creating handle and adding to dict_user
    handle = (name_first + name_last).lower()
    handle = re.sub(r'[^a-z0-9]', '', handle)
    if len(handle) > 20:
        handle = handle[0:20]
    dict_user[handle] = handle
    
    # if list is not empty check for duplicate handles
    number = 0
    if len(initial_object['users']) > 1:
        for user in initial_object['users']:
            if user['handle'] == handle:
                handle = handle + str(number)
                number += 1

    # If list not empty append new dict_user
    if len(initial_object['users']) > 1:
        initial_object['users'].append(dict_user)

    data_store.set(store)

    for user in initial_object['users']:
        for part in user:
            print(f" {part}: {user[part]}")

    return {
        'auth_user_id': user_id,
    }
