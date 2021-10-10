import jwt

SECRET = "CAMEL"

#################################################
######### Helper functions for auth.py ##########
#################################################

# Helper function for auth_register
# Generates a token
def generate_token(auth_user_id):
    global SECRET
    token = jwt.encode({'auth_user_id': auth_user_id}, SECRET, algorithm='HS256')
    return token
    
# Decoding the token
def decode_token(token):
    global SECRET
    decode = jwt.decode(token.encode(), SECRET, algorithms=['HS256'])
    return decode['auth_user_id']
