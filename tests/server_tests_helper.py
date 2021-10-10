import pytest
import requests
import json
from src import config
from src.other import clear_v1

##########################################
############ helper functions ############
##########################################

# Helper function to register a user
def register_user(email, password, name_first, name_last):
    return requests.post(config.url, 'auth/register/v2', {
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

# Helper function to create a channel
def create_channel(token, name, is_public):
    return requests.post(config.url, 'channels/create/v2', {
        'token': token,
        'name': name,
        'is_public': is_public,
    })

# Helper function to invite someone to a channel
def invite_user(user1, channel_id, user2):
    return requests.post(config.url, 'channel/invite/v2', {
        'token': user1.get('token'),
        'channel_id': str(channel_id),
        'u_id': user2.get('u_id')
    })
