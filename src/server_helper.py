import jwt
from src.error import AccessError

SESS_COUNTER = 0
SECRET = "CAMEL"

#################################################
######### Helper functions for auth.py ##########
#################################################

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
    return token
    
# Decoding the token
def decode_token(token):
    global SECRET
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decode['auth_user_id']

# Finding valid user form token
def valid_user(token):
    user_registered = decode_token(token)
    if user_registered is None:
        raise AccessError(description="User does not exist")

    return user_registered