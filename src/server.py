import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config

from src.auth import auth_register_v2, auth_login_v2
from src.channels import channels_listall_v2,channels_create_v2, channels_list_v2
from src.channel import channel_join_v2, channel_details_v2, channel_invite_v2
from src.channel import channel_removeowner_v1, channel_addowner_v1
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
    return dumps (channels_listall_v2(request.args.get('token')))

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

@APP.route("/channels/addowner/v1", methods=['POST'])
def channel_addowner():
    json = request.get_json()
    resp = channel_addowner_v1(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_remove_owner():
    json = request.get_json()
    resp = channel_removeowner_v1(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
