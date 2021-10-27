from datetime import datetime
from os import initgroups
from src.channels import *
from src.auth import *
from src.channel import *
from src.server_helper import *
from src.helper import *
from src.admin import *
from src.user import *
from src.dm import *
from src.message import *
from src.server_helper import *
from src.other import clear_v1
from src.data_store import get_data

'''
id1 = auth_register_v2('anna@gmail.com', 'password', 'afirst', 'afirst')
id2 = auth_register_v2('abc@gmail.com', 'password', 'bfirst', 'bfirst')
id3 = auth_register_v2('cba@gmail.com', 'password', 'cfirst', 'cfirst')
channel = channels_create_v2(id2['token'], 'anna', 'True')
#channel_invite_v2(id2['token'], channel['channel_id'], id1['auth_user_id'])
channel_invite_v2(id2['token'], channel['channel_id'], id3['auth_user_id'])

#channel_addowner_v1(id2['token'], channel['channel_id'], id3['auth_user_id'])
channel_removeowner_v1(id1['token'], channel['channel_id'], id3['auth_user_id'])
'''

clear_v1()
id2 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
id3 = auth_register_v2('cba@gmail.com', 'password', 'cfirst', 'cfirst')
id4 = auth_register_v2('cat@gmail.com', 'password', 'bfirst', 'blast')
channel_id2 = channels_create_v2(id2['token'], 'anna', True)
channel_invite_v2(id2['token'], channel_id2['channel_id'], id3['auth_user_id'])

message_id = message_send_v1(id2['token'], channel_id2['channel_id'], 'hi')
message_id1 = message_send_v1(id2['token'], channel_id2['channel_id'], 'hi1')
message_pin_v1(id2['token'], message_id1['message_id'])

for channel in get_data()['channels']:
    for message in channel['messages']:
        print(message)
'''
channel_invite_v2(id2['token'], channel['channel_id'], id1['auth_user_id'])
channel_invite_v2(id2['token'], channel['channel_id'], id3['auth_user_id'])
print(channel_details_v2(id2['token'], channel['channel_id']))
message_send_v1(id2['token'], channel['channel_id'], 'hihih')
print()
#admin_user_remove_v1(id1['token'], id2['auth_user_id'])
print(channel_messages_v2(id1['token'], channel['channel_id'], 0))
dm_id = dm_create_v1(id2['token'], [id1['auth_user_id']])

print(dm_list_v1(id1['token']))
'''
