from src.data_store import data_store, initial_object
from src.error import InputError
import re

def auth_login_v1(email, password):
    store = data_store.get()
    
    # Iterate through the initial_object list 
    for user in initial_object['users']:
        # If the email and password the user inputs to login match and exist in data_store
        if (user['email'] == email) & (user['password'] == password):
            return user['auth_user_id']
        else:
            raise InputError("Email and/or password is not valid!")

    data_store.set(store)


def auth_register_v1(email, password, name_first, name_last):

    store = data_store.get()

    # Error handling
    token = r'\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b'
    if not (re.search(token, email)):
        raise InputError("This email is of invalid form")

    # Check for duplicate emails
    for user in initial_object['users']:
        if user['email'] == email:
            raise InputError("This email address has already been registered by another user") 

    if len(password) < 6:
         raise InputError("This password is less then 6 characters in length")

    if len(name_first) not in range(1, 51):
         raise InputError("name_first is not between 1 - 50 characters in length")

    if len(name_last) not in range(1, 51):
         raise InputError("name_last is not between 1 - 50 characters in length")
         
    # Creating unique auth_user_id and adding to dict_user
    auth_user_id = len(initial_object['users']) + 1

    # Creating handle and adding to dict_user
    handle = (name_first + name_last).lower()
    handle = re.sub(r'[^a-z0-9]', '', handle)
    if len(handle) > 20:
        handle = handle[0:20]
    
    #Check for duplicate handles
    number = 0
    for user in initial_object['users']:
        if user['handle'] == handle:
            if number == 0: 
                handle = handle +str(number)
            elif number in range(1,10):  
                handle = handle[:-1] + str(number)
            else:
                handle = handle[:-2] + str(number)

        number += 1
                
    # Then append dictionary of user email onto initial_objects

    initial_object['users'].append({
        'email' : email,
        'password': password,
        'name_first': name_first,
        'name_last' : name_last,
        'auth_user_id' : auth_user_id,
        'handle' : handle 
    })

    data_store.set(store)

    return {
        'auth_user_id': auth_user_id,
    }

