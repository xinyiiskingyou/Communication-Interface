'''
Clear the data that has been stored
'''

from src.data_store import DATASTORE, initial_object

def clear_v1():
    '''
    Resets the internal data of the application to its initial state

    Arguments:
        N/A

    Exceptions:
        N/A

    Return Value:
        N/A
    '''
    store = DATASTORE.get()
    initial_object['users'] = []
    initial_object['channels'] = []
    initial_object['dms'] = []
    DATASTORE.set(store)

    return {
    }
