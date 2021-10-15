##########################################
############ users_all tests ##############
##########################################

# Valid case when there is only 1 user
'''def test_user_all_1_member():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    mail1 = requests.get(config.url + "user/all/v1", 
        json = {
        'token': token
    })

    assert (json.loads(mail1.text) == 
    {
        'u_id': json.loads(mail1.text)['auth_user_id'],
        'email': json.loads(mail1.text)['email'],
        'name_first': json.loads(mail1.text)['name_first'],
        'name_last': json.loads(mail1.text)['name_last'],
        'handle_str': json.loads(mail1.text)['handle_str']
    })
    assert len(members) == 1


# Valid case when there is more then 1 user
def test_user_all_several_members():
    requests.delete(config.url + "clear/v1", json={})

    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'email@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user2.json()
    token = user_data['token']

    mail1 = requests.get(config.url + "user/all/v1", 
        json = {
        'token': token
    })

    # test using length of list as cannot be certain 
    # the listed order of users
    members = json.loads(mail1.text)
    assert len(members) == 2


##########################################
########## user_profile tests ############
##########################################

# Input error for invalid u_id
def test_user_profile_invalid_u_id():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abcdef@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'lee'
    })

    user_data = user.json()
    token = user_data['token']

    # Invalid u_id's
    mail1 = requests.get(config.url + "user/profile/v1", 
        json = {
        'token': token,
        'u_id': -1
    })

    mail2 = requests.get(config.url + "user/profile/v1", 
        json = {
        'token': token,
        'u_id': 0
    })

    mail3 = requests.get(config.url + "user/profile/v1", 
        json = {
        'token': token,
        'u_id': 256
    })

    assert mail1.status_code == 400
    assert mail2.status_code == 400
    assert mail3.status_code == 400


##### Implementation #####

# Valid Case
def test_user_profile_valid():
    requests.delete(config.url + "clear/v1", json={})

    user = requests.post(config.url + "auth/register/v2", 
        json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    
    user_data = user.json()
    token = user_data['token']
    u_id = user_data['auth_user_id']

    mail = requests.get(config.url + "user/profile/v1", 
        json = {
        'token': token,
        'u_id': u_id
    })
    
    assert mail.status_code == 200
    assert (json.loads(mail.text) == 
        {
        'user_id': u_id,
        'email': 'abc@gmail.com',
        'name_first': 'anna',
        'name_last': 'park',
        'handle': 'annapark'
    })

if not channels_create_check_valid_user(u_id):
        raise InputError("user is not valid")
    # = decode_token(token)
    
    #user = channels_user_details(u_id)
    return {
        user_info(u_id)
    }

# Returns information about 1 user
@APP.route("/user/profile/v1", methods=['GET'])
def user_profile(): 
    token = (request.args.get('token'))
    u_id = (request.args.get('auth_user_id'))
    return dumps(user_profile_v1(token, u_id))'''


@pytest.fixture
def setup():
    requests.delete(config.url + "clear/v1")

##########################################
######## message/senddm/v1 tests #########
##########################################

# Input Error when channel_id does not refer to a valid channel
# when dm_id is negative
def test_dm_send_invalid_channel_id_positive(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    send_dm = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': -2, 
            'message': 'hello there'
        }
    )
    assert send_dm.status_code == 400


# Input Error when channel_id does not refer to a valid channel
# id is positive integer, but is not an id to any channel
def test_dm_send_invalid_dm_id_nonexistant(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']

    requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    send_dm = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': 256, 
            'message': 'hello there'
        }
    )
    assert send_message.status_code == 400


# Input error when length of message is less than 1 or over 1000 characters
def test_dm_send_invalid_message(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(dm1.text)['dm_id']

    send_dm1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'channel_id': user2_id,
            'message': 'a' * 1001
        }
    )
    assert send_message1.status_code == 400

    send_message2 = requests.post(config.url + "message/send/v1",
        json = {
            'token': user1_token,
            'channel_id': user2_id,
            'message': ''
        }
    )
    assert send_message2.status_code == 400


# Access error when channel_id is valid and the authorised user 
# is not a member of the channel
def test_dm_send_unauthorised_user(setup):
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    user3 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'email@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'park'
        }
    )
    user3_token = json.loads(user3.text)['token']

    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(channel1.text)['dm_id']

    send_message1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user3_token,
            'channel_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_message1.status_code == 403


##### Implementation #####

# Send message in one dm by two users
def test_message_send_valid_one_dm(setup):
    # Register user 1
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    # User 1 creates channel 1
    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(channel1.text)['dm_id']

    # User 1 sends message 1 in channel 1
    send_dm1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_message1.status_code == 200
    json.loads(send_dem1.text)['dm_id']

    # User 2 sends a message in channel 1
    send_dm2 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    json.loads(send_dm2.text)['dm_id']
    assert send_message2.status_code == 200


# Send message in two channels and compare dm message_id to 
# ensure different dm message_id's across different channels
def test_message_send_valid_two_channel(setup):
    # Register user 1
    user1 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'anna@gmail.com',
            'password': 'password',
            'name_first': 'anna',
            'name_last': 'li'
        }
    )
    user1_token = json.loads(user1.text)['token']

    user2 = requests.post(config.url + "auth/register/v2", 
        json = {
            'email': 'sally@gmail.com',
            'password': 'password',
            'name_first': 'sally',
            'name_last': 'li'
        }
    )
    user2_token = json.loads(user2.text)['token']
    user2_id = json.loads(user2.text)['auth_user_id']

    # User 1 creates channel 1
    dm1_create = requests.post(config.url + "dm/create/v1", 
        json = {
            'token': user1_token,
            'u_ids': user2_id,
        }
    )

    dm1_id = json.loads(channel1.text)['dm_id']

    # User 1 sends message 1 in channel 1
    send_dm1 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user1_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_dm1.status_code == 200
    message_dm1 = json.loads(send_dm1.text)['dm_id']

    assert send_message1.status_code == 200
    json.loads(send_dem1.text)['dm_id']

    # User 2 sends a message in channel 1
    send_dm2 = requests.post(config.url + "message/senddm/v1", 
        json = {
            'token': user2_token,
            'dm_id': dm1_id,
            'message': 'hello there'
        }
    )
    assert send_dm2.status_code == 200
    message_dm2 = json.loads(send_dm2.text)['dm_id']

    assert message_dm1 !=  message_dm2


# FUNCTION CODE #

def message_senddm_v1(token, dm_id, message):
    
    auth_user_id = decode_token(token)
    store = DATASTORE.get()

    # Invalid dm_id
    if not check_valid_channel_id(dm_id):
        raise InputError("The dm_id does not refer to a valid dm")

    # Authorised user not a member of channel
    if not check_valid_member_in_channel(dm_id, auth_user_id):
        raise AccessError("Authorised user is not a member of dm with dm_id")

    # Invalid message: Less than 1 or over 1000 characters
    if not check_valid_message(message):
        raise InputError("Message is invalid as length of message is less than 1 or over 1000 characters.")

    # Creating unique message_id 
    dm_id = (len(initial_object['message']) * 2) 

    # Current time message was created and sent
    time_created = time.time()

    dmsend_details = {
        'message_id': message_id,
        'u_id': auth_user_id, 
        'message': message,
        'time_created': time_created
    }

    # Append dictionary of message details into initial_objects['dm']['messages']
    for dm in initial_object['dm']:
        if dm['dm_id'] == dm_id:
            dm['message'].append(dmsend_details)

    # Append dictionary of message details into intital_objects['messages']
    dmsend_details['dm_id'] = dm_id
    initial_object['dm'].append(dmsend_details)

    DATASTORE.set(store)

    return {
        'message_id': dm_id
    }

# SEVER IMPLEMENTATION #
# Send a message from the authorised user to the channel specified by channel_id.
@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    json = request.get_json()
    resp = message_senddm_v1(json['token'], json['dm_id'], json['message'])
    return dumps(resp)
