from json import dumps
import jwt

SECRET = "CAMEL"

#################################################
######### Helper functions for auth.py ##########
#################################################

# Helper function for auth_register
# Generates a token
def generate_token(auth_user_id):
    global SECRET
    return jwt.encode({'auth_user_id': auth_user_id}, SECRET, algorithm='HS256')

# Decoding the token
def decode_token(token):
    global SECRET
    decode = jwt.decode(token.encode(), SECRET, algorithms=['HS256'])
    auth_user_id = int(decode['auth_user_id'])
    return auth_user_id

