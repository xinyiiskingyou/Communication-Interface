import pytest
from src.admin import admin_user_remove_v1, admin_userpermission_change_v1
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.channel import channel_details_v2, channel_invite_v2
from src.channels import channels_create_v2
from src.other import clear_v1
from src.helper import *

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

    # u_id is invalid and authorised user is not a global owner
    user2 = auth_register_v2('cba@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(AccessError):
        admin_user_remove_v1(user2['token'], -1)
    with pytest.raises(AccessError):
        admin_user_remove_v1(user2['token'], -256)

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
        admin_user_remove_v1(user2['token'], user2['auth_user_id'])
    # u_id refers to a user who is the only global owner
    with pytest.raises(AccessError):
        admin_user_remove_v1(user2['token'], user1['auth_user_id'])

def test_admin_remove_valid():
    clear_v1()
    id1 = auth_register_v2('abc@gmail.com', 'password', 'afirst', 'alast')
    id2 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    id3 = auth_register_v2('elephant@gmail.com', 'password', 'cfirst', 'clast')
    id2_info = channels_user_details(id2['auth_user_id'])
    # id1 and id2 create a channel
    channel_id1 = channels_create_v2(id1['token'], 'shelly', False)
    channel_id2 = channels_create_v2(id2['token'], 'anna', True)

    # invite id2 and id3 to id1's channel
    channel_invite_v2(id1['token'], channel_id1['channel_id'], id2['auth_user_id'])
    channel_invite_v2(id1['token'], channel_id1['channel_id'], id3['auth_user_id'])
    id1_detail = channel_details_v2(id1['token'], channel_id1['channel_id'])
    id2_detail = channel_details_v2(id2['token'], channel_id2['channel_id'])

    # remove id2
    admin_user_remove_v1(id1['token'], id2['auth_user_id'])

    # id2 is removed from id1's channel
    assert len(id1_detail['all_members']) == 2
    assert len(id1_detail['owner_members']) == 1

    # id2's channel is empty now
    assert len(id2_detail['all_members']) == 0
    assert len(id2_detail['owner_members']) == 0
    '''
    1. should be removed from all channels/DMs
    2. and will not be included in the list of users returned by users/all.
    3. the contents of the messages they sent will be replaced by 'Removed user'
    4. Streams owners can remove other Streams owners (including the original first owner)
    '''
    
    # name_first should be 'Removed' and name_last should be 'user'.
    assert (id2_info['name_first']) == 'Removed'
    assert (id2_info['name_last']) == 'user'

    # user2's email and handle should be reusable.
    id4 = auth_register_v2('email@gmail.com', 'password', 'bfirst', 'blast')
    channel_invite_v2(id1['token'], channel_id1['channel_id'], id4['auth_user_id'])
    assert len(id1_detail['all_members']) == 3

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

# u_id is invalid the authorised user is not a global owner
# raise Access error in this case
def test_admin_perm_invalid_u_id_and_token():

    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], -1, 1)
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], 'not_an_id', 1)
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], '', 1)

# u_id refers to a user who is the only global owner and they are being demoted to a user
def test_admin_invalid_demote():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user1['auth_user_id'], 2)

def test_admin_invalid_demote1():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    # user1 promotes user2 to be the owner
    admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 1)
    # user2 demotes user1 to be the user
    admin_userpermission_change_v1(user2['token'], user1['auth_user_id'], 2)

    # raise Input error if user2 demotes themselves 
    # since user2 is now the only global owner
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user2['token'], user2['auth_user_id'], 2)

# permission id is invalid 
def test_admin_invalid_permission_id():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], -10)
    with pytest.raises(InputError):
        admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 100)

# permission id is invalid and the authorised user is not a global owner
def test_admin_invalid_permission_id1():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], user1['auth_user_id'], -10)
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], user1['auth_user_id'], 100)

# the authorised user is not a global owner
def test_admin_perm_not_global_owner():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    with pytest.raises(AccessError):
        admin_userpermission_change_v1(user2['token'], user1['auth_user_id'], 2)

# valid case
def test_valid_permission_change():
    clear_v1()
    user1 = auth_register_v2('abc@unsw.edu.au', 'password', 'afirst', 'alast')
    user2 = auth_register_v2('cat@unsw.edu.au', 'password', 'bfirst', 'blast')
    user3 = auth_register_v2('cute@unsw.edu.au', 'password', 'cfirst', 'clast')

    # user2 and user3 have owner permission
    admin_userpermission_change_v1(user1['token'], user2['auth_user_id'], 1)
    admin_userpermission_change_v1(user1['token'], user3['auth_user_id'], 1)
    user2_details = channels_user_details(user2['auth_user_id'])
    user3_details = channels_user_details(user3['auth_user_id'])
    assert user2_details['permission_id'] == 1
    assert user3_details['permission_id'] == 1
    
    # now user3 has permission to demote user2 
    admin_userpermission_change_v1(user3['token'], user2['auth_user_id'], 2)
    assert user2_details['permission_id'] == 2