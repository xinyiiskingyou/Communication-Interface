from src.data_store import initial_object

def check_valid_channel_id(channel_id):
    for channel in initial_object['channels']:
        if int(channel_id) == int(channel['channel_id']):
            return True
    
    return False

def check_valid_member_in_channel(channel_id, auth_user_id):

    # for all channels
    # if the user has channel_id
    # if the users are authorised
    # return True
    for channel in initial_object['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['auth_user_id'] == auth_user_id:
                    return True
    
    return False
