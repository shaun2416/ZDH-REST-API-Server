import cryptography
import jwt
import json

ISSUER = 'sample-auth-server'



ENDPOINT_TO_SCOPE_MAPPING = {
  "get_users" : "read",
  "post_users" : "write", 
  "post_users_json":"write", 
  "resource1_json": "read", 
  "put_users_json": "write",
  "put_users_xml":"write"
}



with open('public.pem', 'rb') as f:
  public_key = f.read()

def verify_access_token(access_token):
  try:
    print("verify_access_token method...")
    decoded_token = jwt.decode(access_token.encode(), public_key,
                               issuer = ISSUER,
                               algorithms = ['RS256'])
    print(f"Decoded token: {decoded_token}")


  except (jwt.exceptions.InvalidTokenError,
          jwt.exceptions.InvalidSignatureError,
          jwt.exceptions.InvalidIssuerError,
          jwt.exceptions.ExpiredSignatureError) as e:
          print(e)
          return False

  return True


def get_scope_of_token(access_token):

  try:

    decoded_token = jwt.decode(access_token.encode(), public_key,
                               issuer = ISSUER,
                               algorithms = ['RS256'])
    print(f"Decoded token: {decoded_token}")

  except (jwt.exceptions.InvalidTokenError,
          jwt.exceptions.InvalidSignatureError,
          jwt.exceptions.InvalidIssuerError,
          jwt.exceptions.ExpiredSignatureError) as e:
          print(e)
          return None
  
  return decoded_token.get("scope")


def validate_token_scope(access_token, endpoint):

  required_scope = ENDPOINT_TO_SCOPE_MAPPING[endpoint]

  decoded_token = jwt.decode(access_token.encode(), public_key,
                               issuer = ISSUER,
                               algorithms = ['RS256'])

  print(f"Access token is {decoded_token}")

  token_scope = decoded_token.get("scope")
  

  if token_scope == "*":
    return True 
  
  return required_scope in token_scope.split()
  

  
  

  
