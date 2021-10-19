import jwt
import time

SESS_COUNTER = 0
SECRET = "CAMEL"

#################################################
######### Helper functions for auth.py ##########
#################################################

valid_token = []

def generate_sess_id():
    global SESS_COUNTER
    SESS_COUNTER += 1
    return SESS_COUNTER

# Helper function for auth_register
# Generates a token
def generate_token(auth_user_id, session_id=None):
    global SECRET
    if session_id is None:
        session_id = generate_sess_id()

    payload = {
        'auth_user_id': auth_user_id,
        'session_id': session_id
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    # append the token in the list
    valid_token.append(token)
    return token
    
# Decoding the token
def decode_token(token):
    global SECRET
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decode['auth_user_id']

# Decode token to find the session_id
def decode_token_session_id(token):
    global SECRET
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decode['session_id']

# Finding valid user form token
def valid_user(token):
    valid_users = valid_token
    for i in range(len(valid_users)):
        # if the token is in the list
        # return the token of the user
        if token in valid_users:
            return valid_users[i]
    return False
