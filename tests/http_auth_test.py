import pytest
import requests
import json
from src import config

##########################################
########### auth_register tests ##########
##########################################

# Input error for invalid email format
def test_reg_invalid_email_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    assert resp1.status_code == 400
    assert resp2.status_code == 400

# Input error for duplicate email
def test_reg_duplicate_email_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    assert resp1.status_code == 200

    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'john',
        'name_last': 'doe'
    }) 
    assert resp2.status_code == 400

# Input error for invalid password
def test_reg_invalid_password_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': '12345',
        'name_first': 'anna',
        'name_last': 'park'
    }) 
    assert resp1.status_code == 400 

# Input error for the name is not between 1 and 50 characters
def test_reg_invalid_name_h():
    requests.delete(config.url + "clear/v1")
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'a' * 53,
        'name_last': 'park'
    }) 
    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'a' * 53
    }) 
    assert resp1.status_code == 400 
    assert resp2.status_code == 400 

##### Implementation #####

# Assert correct return values for auth/register/v2
def test_reg_return_values_h():
    requests.delete(config.url + "clear/v1", json={})
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 
    
    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'email@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 

    token1 = json.loads(resp1.text)['token']
    id1 = json.loads(resp1.text)['auth_user_id']
    token2 = json.loads(resp2.text)['token']
    id2 = json.loads(resp2.text)['auth_user_id']

    assert json.loads(resp1.text) == {'token': token1, 'auth_user_id': id1}
    assert json.loads(resp2.text) == {'token': token2, 'auth_user_id': id2}
    assert id1 != id2
    assert resp1.status_code == 200
    assert resp2.status_code == 200

# test valid handle generation
def test_reg_handle_h():
    requests.delete(config.url + "clear/v1", json={})
    resp1 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 

    resp2 = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abcd@gmail.com',
        'password': 'password',
        'name_first': 'annabelle',
        'name_last': 'parkerparker'
    })

    token1 = json.loads(resp1.text)['token']
    token2 = json.loads(resp2.text)['token']

    profile1 = requests.get(config.url + "users/all/v1", params ={
        'token': token1
    })
    profile2 = requests.get(config.url + "users/all/v1", params ={
        'token': token2
    })  

    handle1 = json.loads(profile1.text)['users'][0]['handle_str']
    assert handle1 == 'annapark'

    handle2 = json.loads(profile2.text)['users'][1]['handle_str']
    assert handle2 == 'annabelleparkerparke'



##########################################
############ auth_login tests ############
##########################################

# Input error when email entered does not belong to a user
def test_login_email_not_belong_to_user():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    resp2 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'def@gmail.dom',
        'password': 'password',
    })
    assert resp2.status_code == 400

# Input error when password is not correct
def test_login_incorrect_password():
    requests.delete(config.url + "clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    resp2 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'wrong password',
    })
    assert resp2.status_code == 400

# valid case
def test_login_valid():
    requests.delete(config.url + "clear/v1", json={})

    # register a new user
    requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    }) 
    login = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'password',
    })
    assert login.status_code == 200

##########################################
############ auth_logout tests ###########
##########################################

# Access error: invalid token
def test_logout_invalid_token():
    requests.delete(config.url + "clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    token = json.loads(user.text)['token']

    logout = requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    assert logout.status_code == 200

    logout1 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token
    })
    assert logout1.status_code == 403

# valid case
def test_logout():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })
    token1 = json.loads(register.text)['token']

    login1 = requests.post(config.url + "auth/login/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
    })
    token2 = json.loads(login1.text)['token']

    login2 = requests.post(config.url + "auth/login/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
    })
    token3 = json.loads(login2.text)['token']

    logout1 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token1
    })
    assert logout1.status_code == 200

    logout2 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token3
    })
    assert logout2.status_code == 200

    logout3 = requests.post(config.url + "auth/logout/v1", json = {
        'token': token2
    })
    assert logout3.status_code == 200


##########################################
#### auth_passwordreset_request tests ####
##########################################

def test_auth_passwordreset_request_valid():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })

    assert pass_request.status_code == 200

##########################################
##### auth_passwordreset_reset tests #####
##########################################

# Input Error: invalid code was given
def test_auth_passwordrequest_reset_invalid_code():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })
    assert json.loads(register.text)['session_list'] == []

    # Check invalid reset code
    pass_reset = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'reset_code': '',
        'new_password': 'new_password'
    })

    assert pass_reset.status_code == 400

# Input Error: password length is < 6 characters long
def test_auth_passwordrequest_reset_invalid_password_length():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })
    assert json.loads(register.text)['session_list'] == []

    # Get reset code
    reset_code = json.loads(register.text)['reset_code']

    # Check invalid password length
    pass_reset = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'reset_code': reset_code,
        'new_password': '12345'
    })

    assert pass_reset.status_code == 400

##### Implementation #####

# Check that they are not able to log in with old password
def test_auth_passwordreset_reset_old():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })

    # Get reset code
    reset_code = json.loads(register.text)['reset_code']

    # Send in the code to the passwordrequest_reset function
    pass_reset = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'reset_code': reset_code,
        'new_password': 'new_password'
    })

    # Check they are logged out of all sessions
    assert pass_reset == 200
    assert json.loads(register.text)['session_list'] == []
    
    # Check old password is invalid
    login = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'password',
    })
    assert login.status_code == 400


# Check that they are able to log in with new password
def test_auth_passwordreset_reset_new():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })

    # Get reset code
    reset_code = json.loads(register.text)['reset_code']

    # Send in the code to the passwordrequest_reset function
    pass_reset = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'reset_code': reset_code,
        'new_password': 'new_password'
    })

    # Check they are logged out of all sessions
    assert pass_reset == 200
    assert json.loads(register.text)['session_list'] == []
    
    # Check new password is valid
    login = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'new_password',
    })
    assert login.status_code == 200

# Check that they are logged out of all sessions
def test_auth_passwordreset_reset_sessions():
    requests.delete(config.url + "clear/v1")
    register = requests.post(config.url + "auth/register/v2", json = {
        'email': 'abc@gmail.com',
        'password': 'password',
        'name_first': 'anna',
        'name_last': 'park'
    })

    # Log user in several times
    login1 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'new_password',
    })
    login2 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'new_password',
    })
    login3 = requests.post(config.url + "auth/login/v2",json = {
        'email': 'abc@gmail.com',
        'password': 'new_password',
    })

    assert len(json.loads(register.text)['session_list']) == 4

    pass_request = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'email': 'abc@gmail.com'
    })

    # Get reset code
    reset_code = json.loads(register.text)['reset_code']

    # Send in the code to the passwordrequest_reset function
    pass_reset = requests.post(config.url + 'auth/passwordreset/request/v1', json = {
        'reset_code': reset_code,
        'new_password': 'new_password'
    })

    # Check they are logged out of all sessions
    assert pass_reset == 200
    assert json.loads(register.text)['session_list'] == []
    