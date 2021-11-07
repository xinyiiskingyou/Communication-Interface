'''
Clear the data that has been stored
'''

from src.data_store import get_data, save

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

    data = get_data()
    data['users'] = []
    data['channels'] = []
    data['dms'] = []
    data['messages'] = []
    data['workspace_stats'] = []
    save()

    return {}
