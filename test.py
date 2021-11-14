import os
import json

def get_data():
    global initial_object
    if os.path.exists('database_test.json'):
        initial_object = json.load(open('database_test.json', 'r'))
    return initial_object

def save(item):
    global initial_object
    with open('database_test.json', 'w') as FILE:
        json.dump(item, FILE)
    print(FILE)
initial_object = {
    'users': [],            # list of dictionaries of users
    'channels': [],         # list of dictionaries of channels
    'messages': [],         # list of dictionaries of messages
    'dms': [],              # list of dictionaries of dms 
    'complete_dms': [],     # list of dictionaries of complete dms
    'workspace_stats': {},  # workspace_stats
}

news = {'user': 1}
get_data()['channels'].append(news) 
save(news)
#print(initial_object)
'''
# orginal what i have
initial_object = {
    'users': [{uer1}, {user2}, {user3}, {user4}],            # list of dictionaries of users
    'channels': [],         # list of dictionaries of channels
    'messages': [],         # list of dictionaries of messages
    'dms': [],              # list of dictionaries of dms 
    'complete_dms': [],     # list of dictionaries of complete dms
    'workspace_stats': {},   # workspace_stats
}


# im gonna create two channels
# orginal what i have
initial_object = {
    'users': [{uer1}, {user2}, {user3}, {user4}],            # list of dictionaries of users
    'channels': [{channel}],         # list of dictionaries of channels
    'messages': [],         # list of dictionaries of messages
    'dms': [],              # list of dictionaries of dms 
    'complete_dms': [],     # list of dictionaries of complete dms
    'workspace_stats': {},   # workspace_stats
}
'''

'''
# im gonna create two channels
# orginal what i have
initial_object = {
    'users': [{uer1}, {user2}, {user3}, {user4}],            # list of dictionaries of users
    'channels': [{channel}],         # list of dictionaries of channels
    'messages': [{message}],         # list of dictionaries of messages
    'dms': [{dm}],              # list of dictionaries of dms 
    'complete_dms': [],     # list of dictionaries of complete dms
    'workspace_stats': {},   # workspace_stats
}

'''