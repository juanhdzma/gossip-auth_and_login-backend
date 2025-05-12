from datetime import datetime,timedelta, timezone
from fastapi import Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import requests
from src.infrastructure.Envs import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

class AccessTokenHelper:
    @staticmethod
    def createAccessToken(email: str, username:str):
        exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        accessTokenToEncode = {"email": email, "username":username, "exp":exp}
        return jwt.encode(accessTokenToEncode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verifyAccessToken(authCredentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        try:
            payload = jwt.decode(authCredentials.credentials, SECRET_KEY, algorithms=ALGORITHM)
            return payload
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.exceptions.InvalidTokenError as e:
            print(e)
            raise HTTPException(status_code=401, detail="Invalid access token")
        
class AccessTokenGoogleHelper:
    @staticmethod
    def decodeAccessToken(accessToken: str) -> Response:
        URL = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {
            'Authorization': f'Bearer {accessToken}'
        }
        response = requests.get(URL, headers=headers)
        print("result got: ", response)
        return response.json() 
            

        



