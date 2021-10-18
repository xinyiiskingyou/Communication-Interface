import jwt
import time
from src.error import AccessError
SECRET = "CAMEL"

#################################################
######### Helper functions for auth.py ##########
#################################################

valid_token = []

# Helper function for auth_register
# Generates a token
def generate_token(auth_user_id):
    global SECRET
    payload = {
        'auth_user_id': auth_user_id,
        'timestamp': time.time()
    }
    token = str(jwt.encode(payload, SECRET, algorithm='HS256'))
    # append the token in the list
    valid_token.append(token)
    return token
    
# Decoding the token
def decode_token(token):
    global SECRET
    decode = jwt.decode(token.encode(), SECRET, algorithms=['HS256'])
    return decode['auth_user_id']

# Finding valid user from token
def valid_user(token):
    valid_users = valid_token
    for i in range(len(valid_users)):
        # if the token is in the list
        # return the token of the user
        if token in valid_users:
            return valid_users[i]
    return False
