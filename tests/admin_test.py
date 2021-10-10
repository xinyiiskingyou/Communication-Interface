import pytest
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_join_v2
from src.channels import channels_create_v2
from src.other import clear_v1

##########################################
######## admin_user_remove tests #########
##########################################

# u_id does not refer to a valid user
def test_admin_remove_invalid_u_id():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        admin_user_remove_v1(user1['token'], -1)
    with pytest.raises(InputError):
        admin_user_remove_v1(user1['token'], 'not_an_id')
    with pytest.raises(InputError):
        admin_user_remove_v1(user1['token'], '')

# u_id refers to a user who is the only global owner
def test_admin_global_owner():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        admin_user_remove_v1(user1['token'], user1['auth_user_id'])

# the authorised user is not a global owner
def test_admin_remove_not_global_owner():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(AccessError):
        admin_user_remove_v1(user2['token'], user1['auth_user_id'])

def test_admin_remove_valid():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    user3 = auth_register_v2('cute@unsw.edu.au', 'password', 'cfirst', 'clast')

    # user1 and user2 create a channel
    channel_id = channels_create_v2(user1['token'], 'shelly', True)
    channel_id1 = channels_create_v2(user2['token'], 'sally', True)

    # user2 and user3 join user1's channel
    channel_join_v2(user2['token'], channel_id['channel_id'])
    channel_join_v2(user3['token'], channel_id['channel_id'])

    # remove user2
    admin_user_remove_v1(user1['token'], user2['auth_user_id'])
    # user 2 is removed from channel
    details = channel_details_v2(user1['token'], channel_id['channel_id'])
    assert len(details['all_members']) == 2

    # user2's channel should have no member now
    details1 = channel_details_v2(user2['token'], channel_id1['channel_id'])
    assert len(details1['owner_members']) == 0
    assert len(details1['all_members']) == 0
    
    '''
    1. should be removed from all channels/DMs
    2. and will not be included in the list of users returned by users/all.
    3. the contents of the messages they sent will be replaced by 'Removed user'
    4. Streams owners can remove other Streams owners (including the original first owner)
    '''
    
    # name_first should be 'Removed' and name_last should be 'user'.
    assert (details1['owner_members'][0]['name_first']) == 'Removed'
    assert (details1['owner_members'][0]['name_last']) == 'user'

    # user2's email and handle should be reusable.
    user4 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    channel_join_v2(user4['token'], channel_id['channel_id'])
    assert len(details['all_members']) == 3

##########################################
#### admin_userpermission_change tests ###
##########################################

# u_id does not refer to a valid user
def test_admin_perm_invalid_u_id():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], -1, 1)
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], 'not_an_id', 1)
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], '', 1)

# u_id refers to a user who is the only global owner and they are being demoted to a user
def test_admin_perm_demote():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    admin_userpermission_change_v1(user1['token'], user1['auth_user_id'], 2)
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user1['auth_user_id'], 2)

# permission_id is invalid
def test_admin_perm_global_owner():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user2['auth_uer_id'] -10)
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 100)

# the authorised user is not a global owner
def test_admin_perm_not_global_owner():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], user1['auth_user_id'], 2)

def test_valid_permission_change():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    user3 = auth_register_v2('cute@unsw.edu.au', 'password', 'cfirst', 'clast')

    # user2 and user3 have owner permission
    admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 1)
    admin_userpermission_change_v1(user1['token'], user3['auth_user_id'], 1)

    # demote user2 
    admin_userpermission_change_v1(user3['token'], user2['auth_user_id'], 2)