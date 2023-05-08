import cryptography
import jwt
import json

ISSUER = 'sample-auth-server'



ENDPOINT_TO_SCOPE_MAPPING = {
  "get_users" : "read"
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
  
  access_token = access_token.replace("'", '"')

  token_scope = json.loads(access_token).get("scope")

  if token_scope == "*":
    return True 
  
  return required_scope in token_scope.split()
  

  
  

  
