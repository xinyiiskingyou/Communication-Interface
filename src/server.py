import json
import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_listall_v2,channels_create_v2, channels_list_v2
from src.channel import channel_join_v2, channel_details_v2, channel_invite_v2, channel_leave_v1
from src.channel import channel_removeowner_v1, channel_addowner_v1, channel_messages_v2
from src.user import user_profile_sethandle_v1, user_profile_setemail_v1, user_profile_setname_v1
from src.message import message_send_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, message_senddm_v1
from src.other import clear_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# To clear the data
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    resp = clear_v1()
    return dumps(resp)


############ AUTH #################

# Registers user
@APP.route("/auth/register/v2", methods=['POST'])
def register(): 
    json = request.get_json()
    resp = auth_register_v2(json['email'], json['password'], json['name_first'], json['name_last'])
    return dumps({
        'token': resp['token'],
        'auth_user_id': resp['auth_user_id']
    })

# Logins user 
@APP.route("/auth/login/v2", methods=['POST'])
def login():
    json = request.get_json()
    resp = auth_login_v2(json['email'], json['password'])
    return dumps({
        'token': resp['token'],
        'auth_user_id': resp['auth_user_id']
    })


############ CHANNELS #################

# channel create
@APP.route("/channels/create/v2", methods=['POST'])
def channel_create():
    json = request.get_json()
    resp = channels_create_v2(json['token'], json['name'], json['is_public'])
    return dumps({
        'channel_id': resp['channel_id']
    })

# Return the list that authorised user is part of
@APP.route("/channels/list/v2", methods=['GET'])
def channels_list(): 
    return dumps(channels_list_v2(request.args.get('token')))

# return the list of all channels
@APP.route ("/channels/listall/v2", methods= ['GET'])
def listall():
    return dumps(channels_listall_v2(request.args.get('token')))


############ CHANNEL #################

# Invite user to join the channel
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    json = request.get_json()
    resp = channel_invite_v2(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

# join wrap?   
@APP.route ("/channel/join/v2", methods= ['POST'])
def channel_join():
    json = request.get_json()
    resp1 = channel_join_v2(json['token'], json['channel_id'])
    return dumps (resp1)

# Gives details about channel
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details(): 
    token = (request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_details_v2(token, channel_id))
   
# Add an owner of the channel
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    json = request.get_json()
    resp = channel_addowner_v1(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

# Remove an owner of the channel
@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    json = request.get_json()
    resp = channel_removeowner_v1(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

# Given a channel with ID channel_id that the authorised user is a member of, 
# remove them as a member of the channel
@APP.route("/channel/leave/v1", methods= ['POST'])
def channel_leave(): 
    json = request.get_json()
    resp = channel_leave_v1(json['token'], json['channel_id'])
    return dumps(resp)

# Given a channel with ID channel_id that the authorised user is a member of, 
# return up to 50 messages between index "start" and "start + 50"
@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    token = (request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return dumps(channel_messages_v2(token, channel_id, start))


############ USER #################

# Update the authorised user's first and/or last name
@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_setename(): 
    json = request.get_json()
    resp = user_profile_setname_v1(json['token'], json['name_first'], json['name_last'])
    return dumps(resp)

# Update the authorised user's email
@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_setemail(): 
    json = request.get_json()
    resp = user_profile_setemail_v1(json['token'], json['email'])
    return dumps(resp)

# Update the authorised user's handle
@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_sethandle(): 
    json = request.get_json()
    resp = user_profile_sethandle_v1(json['token'], json['handle_str'])
    return dumps(resp)


############ MESSAGE ############

# Send a message from the authorised user to the channel specified by channel_id.
@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    json = request.get_json()
    resp = message_send_v1(json['token'], json['channel_id'], json['message'])
    return dumps(resp)


############ DM #################
@APP.route("/dm/details/v1", methods=['GET'])
def dm_details(): 
    token = (request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    return dumps(dm_details_v1(token, dm_id))

# Create DM
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    json = request.get_json()
    resp = dm_create_v1(json['token'], json['u_ids'])
    return dumps({
        'dm_id': resp['dm_id']
    })

# List al DMs that the user is a member of
@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    return dumps(dm_list_v1(request.args.get('token')))

# Remove DM that the user if the creator of
@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    json = request.get_json()
    resp = dm_remove_v1(json['token'], json['dm_id'])
    return dumps(resp)

# Send a message from the authorised user to the channel specified by dm_id.
@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    json = request.get_json()
    resp = message_senddm_v1(json['token'], json['dm_id'], json['message'])
    return dumps(resp)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
