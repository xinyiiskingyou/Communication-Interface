'''
Clear the data that has been stored
'''

from src.data_store import DATASTORE, initial_object

def clear_v1():
    '''
    Clear the data that has been stored
    '''
    store = DATASTORE.get()
    initial_object['users'] = []
    initial_object['channels'] = []
    DATASTORE.set(store)

    return {
    }
