'''
Notifications implementation
'''

from src.data_store import get_data, save
from src.error import InputError, AccessError
from src.helper import channel_dm_of_message_id, u_id_to_handle_str, channel_id_to_channel_name, dm_id_to_dm_name
from src.server_helper import decode_token, valid_user

TAG_START = 0
TAG_END = 20

# Activates a notification if either of these 3 cases occur: 
    # 1. Authorised user of channel is tagged by other member in a message in channel/DM
    # 2. Valid member of channel reacts to authorised user's message in channel/DM
    # 3. Authorised user is invited to a channel or is added to a DM

# Sends notification for when a user is tagged in a channel they are a member of 
# auth_user_id is the user that completed the above action to activate the notification
# handle_str_list is the list of users the notification is going to be sent to
def activate_notification_tag_channel(auth_user_id, handle_str_list, channel_id, message):
    # print(f"handle_str_list {handle_str_list}")

    handle_str_notif_from = u_id_to_handle_str(auth_user_id)

    channel_name = channel_id_to_channel_name(channel_id)
        
    notification_message = f"{handle_str_notif_from} tagged you in {channel_name}: {message[TAG_START:TAG_END]}"

    notification = {
        'channel_id': channel_id,
        'dm_id': -1,
        'notification_message': notification_message
    }

    for tagged_user in handle_str_list:
        for user2 in get_data()['users']:
            # print(f"handle1 {user2['handle_str']}")
            # print(f"tagged user {tagged_user}")
            if user2['handle_str'] == tagged_user:
                # print("HELLO")
                user2['all_notifications'].insert(0, notification)
                save()

# Sends notification for when a user is tagged in a DM they are a member of
def activate_notification_tag_dm(auth_user_id, handle_str_list, dm_id, message):

    handle_str_notif_from = u_id_to_handle_str(auth_user_id)

    dm_name = dm_id_to_dm_name(dm_id)
        
    notification_message = f"{handle_str_notif_from} tagged you in {dm_name}: {message[TAG_START:TAG_END]}"

    notification = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': notification_message
    }

    for tagged_user in handle_str_list:
        for user2 in get_data()['users']:
            # print(f"handle1 {user2['handle_str']}")
            # print(f"tagged user {tagged_user}")
            if user2['handle_str'] == tagged_user:
                # print("HELLO")
                user2['all_notifications'].insert(0, notification)
                save()

# Sends notification for when a user reacts to a message
def activate_notification_react(auth_user_id, message_id):

    # channel_dm_id -> id of channel/DM containing message_id
    # u_id -> user that sent the message and which the notification is going to be sent to
    channel_dm_id = channel_dm_of_message_id(message_id)['channel_dm_id']
    u_id = channel_dm_of_message_id(message_id)['u_id']

    # Find the handle_str of auth_user_id -> user that activated the notification
    handle_str_notif_from = u_id_to_handle_str(auth_user_id)

    if message_id % 2 == 1:
        # Message reacted is from channel
        channel_name = channel_id_to_channel_name(channel_dm_id)

        notification_message = f"{handle_str_notif_from} reacted to your message in {channel_name}"

        notification = {
            'channel_id': channel_dm_id,
            'dm_id': -1,
            'notification_message': notification_message
        }

        for user in get_data()['users']:
            if user['auth_user_id'] == u_id:
                user['all_notifications'].insert(0, notification)
                save()

    elif message_id % 2 == 0:
        # Message reacted is from DM
        dm_name = dm_id_to_dm_name(channel_dm_id)

        notification_message = f"{handle_str_notif_from} reacted to your message in {dm_name}"

        notification = {
            'channel_id': -1,
            'dm_id': channel_dm_id,
            'notification_message': notification_message
        }

        for user in get_data()['users']:
            if user['auth_user_id'] == u_id:
                user['all_notifications'].insert(0, notification)
                save()

# Sends notification for when a user invites another to a channel
def activate_notification_channel_invite(auth_user_id, channel_id, u_id):

    channel_name = channel_id_to_channel_name(channel_id)
    
    # Find the handle_str of auth_user_id -> user that activated the notification
    handle_str_notif_from = u_id_to_handle_str(auth_user_id)

    notification_message = f"{handle_str_notif_from} added you to {channel_name}"

    notification = {
        'channel_id': channel_id,
        'dm_id': -1,
        'notification_message': notification_message
    }

    for user in get_data()['users']:
        if user['auth_user_id'] == u_id:
            user['all_notifications'].insert(0, notification)
            save()

def activate_notification_dm_create(auth_user_id, dm_id, member_list):

    dm_name = dm_id_to_dm_name(dm_id)

    handle_str_notif_from = u_id_to_handle_str(auth_user_id)

    notification_message = f"{handle_str_notif_from} added you to {dm_name}"

    notification = {
        'channel_id': -1,
        'dm_id': dm_id,
        'notification_message': notification_message
    }

    for dm_member in member_list:
        if dm_member['u_id'] != auth_user_id:
            for user in get_data()['users']:
                if user['auth_user_id'] == dm_member['u_id']:
                    user['all_notifications'].insert(0, notification)
                    save()


def notifications_get_v1(token):
    auth_user_id = decode_token(token)

    for user in get_data()['users']:
        if user['auth_user_id'] == auth_user_id:
            notifications = user['all_notifications'][0:20]

    print(notifications)

    return {
        'notifications': notifications
    }