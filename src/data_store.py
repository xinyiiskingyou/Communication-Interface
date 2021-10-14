'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [], # create a dict in a list
    'messages': [] # list of dictionaries of messages
}

## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    '''
    Datastore class used to store your data
    '''
    def __init__(self):
        self.__store = initial_object

    def get(self):
        '''
        Get the data store in initial object
        '''
        return self.__store

    def set(self, store):
        '''
        Set the data store in initial object
        '''
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

DATASTORE = Datastore()



