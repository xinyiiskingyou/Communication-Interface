import pytest
from src.channel import channel_messages_v2
from src.error import InputError, AccessError
from src.channels import channels_create_v2
from src.auth import auth_register_v2
from src.other import clear_v1


##########################################
######### channel_messages tests #########
##########################################

# channel_id does not refer to a valid channel
def test_messages_invalid_channel_id():
    clear_v1()
    id4 = auth_register_v2('cat@gmail.com', 'password', 'afirst', 'alast')

    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], -16, 0)
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], 0, 0)
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], 256, 0)
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], 'not_an_id', 0)
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], '', 0)


# channel_id is valid and the authorised user is not a member of the channel 
def test_messages_user_not_authorised_to_channel():
    clear_v1()
    id3 = auth_register_v2('elephant@gmail.com', 'password', 'afirst', 'alast')
    id4 = auth_register_v2('cat@gmail.com', 'password', 'bfirst', 'blast')
    channel_id4 = channels_create_v2(id4['token'], 'shelly', False)

    with pytest.raises(AccessError):
        channel_messages_v2(id3['token'], channel_id4['channel_id'], 0)

    # Above condition and Invalid start
    # Raises Access Error as it raises both Input and Access Error
    with pytest.raises(AccessError):
        channel_messages_v2(id3['token'], channel_id4['channel_id'], 256)   
    with pytest.raises(AccessError):
        channel_messages_v2(id3['token'], channel_id4['channel_id'], 'not_valid')


# Start is not a valid positive integer
def test_messages_invalid_start():
    clear_v1()
    id4 = auth_register_v2('cat@gmail.com', 'password', 'afirst', 'alast')
    channel_id4 = channels_create_v2(id4['token'], 'shelly', False)

    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], channel_id4['channel_id'], -16)
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], channel_id4['channel_id'], 256)
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], channel_id4['channel_id'], 'not_an_id')
    with pytest.raises(InputError):
        channel_messages_v2(id4['token'], channel_id4['channel_id'], '')


##### Implementation ##### 

# Start at most recent message (index = 0) and number of messages > 50


# Start at most recent message (index = 0) and number of messages < 50


# Start at most recent message (index = 0) and number of messages = 50


# Start at neither most or least recent and number of messages > 50


# Start at neither most or least recent and number of messages < 50


# No messages currently in channel
def test_messages_empty():
    clear_v1()
    id4 = auth_register_v2('cat@gmail.com', 'password', 'afirst', 'alast')
    channel_id4 = channels_create_v2(id4['token'], 'shelly', False)

    assert (channel_messages_v2(id4['token'], channel_id4['channel_id'], 0) == 
        {
            'messages' :[],
            'start': 0, 
            'end': -1
        }
    )

