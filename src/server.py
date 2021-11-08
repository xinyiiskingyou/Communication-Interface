import signal
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.error import InputError
from src import config

from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.channels import channels_listall_v2,channels_create_v2, channels_list_v2
from src.channel import channel_join_v2, channel_details_v2, channel_invite_v2, channel_leave_v1
from src.channel import channel_removeowner_v1, channel_addowner_v1, channel_messages_v2
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, message_senddm_v1, dm_messages_v1, dm_leave_v1
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_react_v1, message_unreact_v1, message_pin_v1
from src.message import message_unpin_v1, message_sendlater_v1, message_sendlaterdm_v1, message_share_v1
from src.user import user_profile_sethandle_v1, user_profile_setemail_v1, user_profile_setname_v1, user_profile_v1, users_all_v1
from src.user import user_stats_v1, user_profile_uploadphoto_v1
from src.notifications import notifications_get_v1
from src.search import search_v1
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

APP = Flask(__name__, static_url_path='/static/')
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
# Given a registered user's email and password, returns their `token` value.
@APP.route("/auth/login/v2", methods=['POST'])
def login():
    json = request.get_json()
    resp = auth_login_v2(json['email'], json['password'])
    return dumps({
        'token': resp['token'],
        'auth_user_id': resp['auth_user_id']
    })

# Logouts user
# Given an active token, invalidates the token to log the user out.
@APP.route("/auth/logout/v1", methods=['POST'])
def logout():
    json = request.get_json()
    resp = auth_logout_v1(json['token'])
    return dumps(resp)

# Creates a random string of letters and numbers
# Used to validify a user when reseting password
@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def pass_request():
    json = request.get_json()
    resp = auth_passwordreset_request_v1(json['email'])
    return dumps(resp)

# Uses code from passwordreset_request to change password
@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def pass_reset():
    json = request.get_json()
    resp = auth_passwordreset_reset_v1(json['reset_code'], json['new_password'])
    return dumps(resp)

############ CHANNELS #################

# Creates a new channel with the given name that is either a public or private channel. 
@APP.route("/channels/create/v2", methods=['POST'])
def channel_create():
    json = request.get_json()
    resp = channels_create_v2(json['token'], json['name'], json['is_public'])
    return dumps({
        'channel_id': resp['channel_id']
    })

# Provide a list of all channels (and their associated details) 
# that the authorised user is part of.
@APP.route("/channels/list/v2", methods=['GET'])
def channels_list(): 
    return dumps(channels_list_v2(request.args.get('token')))

# Provide a list of all channels, including private channels, 
# (and their associated details)
@APP.route ("/channels/listall/v2", methods= ['GET'])
def listall():
    return dumps(channels_listall_v2(request.args.get('token')))

############ CHANNEL #################

# Invite new user to the channel
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    json = request.get_json()
    resp = channel_invite_v2(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

# Add the user to the channel
@APP.route ("/channel/join/v2", methods= ['POST'])
def channel_join():
    json = request.get_json()
    resp1 = channel_join_v2(json['token'], json['channel_id'])
    return dumps(resp1)

# Provide basic details about the channel.
@APP.route("/channel/details/v2", methods=['GET'])
def channel_details(): 
    token = (request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    return dumps(channel_details_v2(token, channel_id))
   
# Make user with user id u_id an owner of the channel
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    json = request.get_json()
    resp = channel_addowner_v1(json['token'], json['channel_id'], json['u_id'])
    return dumps(resp)

# Remove user with user id u_id as an owner of the channel
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

############ USERS #################

# Returns information about all users
@APP.route("/users/all/v1", methods=['GET'])
def user_all(): 
    token = (request.args.get('token'))
    return dumps(users_all_v1(token))

############## USER #################

# Returns information about 1 user
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile(): 
    result = user_profile_v1(request.args.get('token'), request.args.get('u_id'))
    return dumps(result)

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

# Returns information about 1 user
@APP.route("/user/stats/v1", methods=['GET'])
def user_stats(): 
    result = user_stats_v1(request.args.get('token'))
    return dumps(result)

# Uploads given photo to given dimensions
@APP.route('/user/profile/uploadphoto/v1', methods=['POST'])
def user_uploadphoto():
    json = request.get_json()
    resp = user_profile_uploadphoto_v1(json['token'], json['img_url'], json['x_start'], json['y_start'], json['x_end'], json['y_end'])
    return dumps(resp)

@APP.route('/static/<path:path>', methods = ['GET'])
def display_photo(path):
    return send_from_directory('', path)

############ MESSAGE ############

# Send a message from the authorised user to the channel specified by channel_id.
@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    json = request.get_json()
    resp = message_send_v1(json['token'], json['channel_id'], json['message'])
    return dumps(resp)

# Given a message, update its text with new text. 
# If the new message is an empty string, the message is deleted.
@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    json = request.get_json()
    resp = message_edit_v1(json['token'], json['message_id'], json['message'])
    return dumps(resp)

# Given a message_id for a message, this message is removed from the channel/DM
@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    json = request.get_json()
    resp = message_remove_v1(json['token'], json['message_id'])
    return dumps(resp)

# Send a message from the authorised user to the channel specified by dm_id.
@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    json = request.get_json()
    resp = message_senddm_v1(json['token'], json['dm_id'], json['message'])
    return dumps(resp)

# Add a "react" to that particular message.
@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    json = request.get_json()
    resp = message_react_v1(json['token'], json['message_id'], json['react_id'])
    return dumps(resp)

# Remove a "react" to that particular message.
@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    json = request.get_json()
    resp = message_unreact_v1(json['token'], json['message_id'], json['react_id'])
    return dumps(resp)

# Given a message within a channel or DM, mark it as "pinned".
@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    json = request.get_json()
    resp = message_pin_v1(json['token'], json['message_id'])
    return dumps(resp)

# Given a message within a channel or DM, remove its mark as "pinned".
@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    json = request.get_json()
    resp = message_unpin_v1(json['token'], json['message_id'])
    return dumps(resp)

# Send a message from auth_user to the channel automatically at a specified time in the future
@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    json = request.get_json()
    resp = message_sendlater_v1(json['token'], json['channel_id'], json['message'], json['time_sent'])
    return dumps(resp)

# Send a message from auth_user to the dm automatically at a specified time in the future
@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    json = request.get_json()
    resp = message_sendlaterdm_v1(json['token'], json['dm_id'], json['message'], json['time_sent'])
    return dumps(resp)

# Message is shared to another channel/DM. An optional message can be added 
# onto the shared message
@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    json = request.get_json()
    resp = message_share_v1(json['token'], json['og_message_id'], json['message'], json['channel_id'], json['dm_id'])
    return dumps(resp)

############ DM #################

# Return basic details about the DM
@APP.route("/dm/details/v1", methods=['GET'])
def dm_details(): 
    token = (request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    return dumps(dm_details_v1(token, dm_id))

# Create new DM
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    json = request.get_json()
    resp = dm_create_v1(json['token'], json['u_ids'])
    return dumps({
        'dm_id': resp['dm_id']
    })

# Given a DM with ID dm_id that the authorised user is a member of, 
# return up to 50 messages between index "start" and "start + 50"
@APP.route ("/dm/messages/v1", methods=['GET'])
def dm_message(): 
    token = (request.args.get('token'))
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    return dumps(dm_messages_v1(token, dm_id, start))

# Returns the list of DMs that the user is a member of
@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    return dumps(dm_list_v1(request.args.get('token')))

# Remove DM that the user if the creator of
@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    json = request.get_json()
    resp = dm_remove_v1(json['token'], json['dm_id'])
    return dumps(resp)

# Remove user as a member of the DM
@APP.route ("/dm/leave/v1", methods = ['POST'])
def dm_leave(): 
    json = request.get_json()
    resp = dm_leave_v1(json['token'], json['dm_id'])
    return dumps(resp)

############ ADMIN #################

# Given a user by their u_id, remove them from the Streams
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove():
    json = request.get_json()
    resp = admin_user_remove_v1(json['token'], json['u_id'])
    return dumps(resp)

# Given a user by their user ID, set their permissions to new 
# permissions described by permission_id
@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission():
    json = request.get_json()
    resp = admin_userpermission_change_v1(json['token'], json['u_id'], json['permission_id'])
    return dumps(resp)


############ NOTIFICATIONS #################

# Return the user's most recent 20 notifications, ordered from most recent to least recent.
@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get():
    token = (request.args.get('token'))
    return dumps(notifications_get_v1(token))


############ SEARCH #################

# Given a query string, return a collection of messages in all of the channels/DMs that the
# user has joined that contain the query.
@APP.route("/search/v1", methods=['GET'])
def search():
    token = (request.args.get('token'))
    query_str = (request.args.get('query_str'))
    return dumps(search_v1(token, query_str))

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
