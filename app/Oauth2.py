from cmath import exp
from datetime import timedelta, datetime
from os import stat
import re
from fastapi import Depends, status, HTTPException
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from config import settings
# This is the secret key used to sign the JWT
#I Created The secret key using the following command: openssl rand -hex 32
#if it wasn't recognized, then go to the location where you installd openssl and run the command again.
#I installed openssl in D:Programs\openssl\bin
SECRET_KEY = settings.SECRET_KEY
#this is the algorithm used to sign the JWT
ALGORITHM = settings.ALGORITHM

#this is the time in minutes that the access token will be valid for
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#extracts the informatino from the token then gets the id from the token_data
def verify_access_token(token: str, credentials_exception: Exception = None):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except jwt.JWTError:
        raise credentials_exception
    return token_data

#this the functions that validates the token and gets the user. 
#it validates the user by getting the imbedded user_id from the token
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Invalid credentials",headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user