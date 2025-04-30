from datetime import datetime,timedelta, timezone
from fastapi import Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import requests
from src.infrastructure.Envs import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

class AccessTokenHelper:
    @staticmethod
    def create_access_token(email: str, username:str):
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        accessTokenToEncode = {"email": email, "username":username, "exp":expires_at}
        return jwt.encode(accessTokenToEncode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_access_token(auth_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = jwt.decode(auth_credentials.credentials, SECRET_KEY, algorithms=ALGORITHM)
            return payload
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.exceptions.InvalidTokenError as e:
            print(e)
            raise HTTPException(status_code=401, detail="Invalid access token")
        
class AccessTokenGoogleHelper:
    @staticmethod
    def decode_access_token(access_token: str) -> Response:
        URL = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(URL, headers=headers)
        print("result got: ", response)
        return response.json() 
            

        



