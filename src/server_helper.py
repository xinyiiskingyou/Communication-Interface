import jwt

SESS_COUNTER = 0
SECRET = "CAMEL"

from src.data_store import get_data

# Generates session id 
def generate_sess_id():
    global SESS_COUNTER
    SESS_COUNTER += 1
    return SESS_COUNTER

# Helper function for auth_register
# Generates a token
def generate_token(auth_user_id, session_id=None):
    global SECRET
    # if session_id is None:
    #    session_id = generate_sess_id()

    payload = {
        'auth_user_id': auth_user_id,
        'session_id': session_id
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token
    
# Decoding the token and returning the auth_user_id
def decode_token(token):
    global SECRET
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decode['auth_user_id']

# Decoding the token and returning the session_id
def decode_token_session_id(token):
    global SECRET
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decode['session_id']

# Check token is valid with valid session_id
def valid_user(token):
    for user in get_data()['users']:
        if user['auth_user_id'] == decode_token(token):
            for session in range(len(user['session_list'])):
                if (user['session_list'][session]) == decode_token_session_id(token):
                    return True
    return False
