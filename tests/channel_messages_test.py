import pytest
from src.channel import channel_messages_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1


##########################################
######### channel_messages tests #########
##########################################

# Invalid auth_user_id
def test_messages_auth_user_id():
    clear_v1()
    id2 = auth_register_v1('email@gmail.com', 'password', 'afirst', 'alast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'bfirst', 'blast')
    channel_id2 = channels_create_v1(id2['auth_user_id'], 'anna', True)
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    # Public
    with pytest.raises(AccessError):
        channel_messages_v1(-16, channel_id2['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1(0, channel_id2['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1(256, channel_id2['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1('not_an_id', channel_id2['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1('', channel_id2['channel_id'], 0)

    # Private
    with pytest.raises(AccessError):
        channel_messages_v1(-16, channel_id4['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1(0, channel_id4['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1(256, channel_id4['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1('not_an_id', channel_id4['channel_id'], 0)
    with pytest.raises(AccessError):
        channel_messages_v1('', channel_id4['channel_id'], 0)

    # Invalid auth_user_id and Invalid channel_id
    # Raises Access Error because it raises Input and Access Error 
    with pytest.raises(AccessError):
        channel_messages_v1(-16, -16, 0)  
    with pytest.raises(AccessError):
        channel_messages_v1(0, '', 0)  

    # Invalid auth_user_id and Invalid_start
    # Raises Access Error because it raises Input and Access Error 
    with pytest.raises(AccessError):
        channel_messages_v1(0, channel_id4['channel_id'], 256)   
    with pytest.raises(AccessError):
        channel_messages_v1(-256, channel_id4['channel_id'], 'not_valid') 


# channel_id does not refer to a valid channel
def test_invalid_channel_id():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'afirst', 'alast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], -16, 0)
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], 0, 0)
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], 256, 0)
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], 'not_an_id', 0)
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], '', 0)


# channel_id is valid and the authorised user is not a member of the channel 
def test_user_not_authorised_to_channel():
    clear_v1()
    id3 = auth_register_v1('elephant@gmail.com', 'password', 'afirst', 'alast')
    id4 = auth_register_v1('cat@gmail.com', 'password', 'bfirst', 'blast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(AccessError):
        channel_messages_v1(id3['auth_user_id'], channel_id4['channel_id'], 0)

    # Above condition and Invalid start
    # Raises Access Error as it raises both Input and Access Error
    with pytest.raises(AccessError):
        channel_messages_v1(id3['auth_user_id'], channel_id4['channel_id'], 256)   
    with pytest.raises(AccessError):
        channel_messages_v1(id3['auth_user_id'], channel_id4['channel_id'], 'not_valid')


# Start is not a valid positive integer
def test_invalid_start():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'afirst', 'alast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], -16)
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], 256)
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], '')


##### Implementation ##### (To be completed when adding messages is added)

# Start at most recent message (index = 0) and number of messages > 50


# Start at most recent message (index = 0) and number of messages < 50


# Start at most recent message (index = 0) and number of messages = 50


# Start at neither most or least recent and number of messages > 50


# Start at neither most or least recent and number of messages < 50


# No messages currently in channel
def test_no_messages():
    clear_v1()
    id4 = auth_register_v1('cat@gmail.com', 'password', 'afirst', 'alast')
    channel_id4 = channels_create_v1(id4['auth_user_id'], 'shelly', False)

    assert (channel_messages_v1(id4['auth_user_id'], channel_id4['channel_id'], 0) == 
        {
            'messages' :[],
            'start': 0, 
            'end': -1
        }
    )

