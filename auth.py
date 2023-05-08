import cryptography
import jwt

ISSUER = 'sample-auth-server'

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
  

  
