from wsgiref import validate
from fastapi import APIRouter, Depends, Response, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from typing import List, Optional
import utils, Oauth2

router = APIRouter( )

@router.post("/",status_code= status.HTTP_200_OK,response_model=schemas.Token)
async def login(userCredentials: OAuth2PasswordRequestForm = Depends(),  db:Session = Depends(get_db)):
   
    db_user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    if not utils.verify_password(plain_password=userCredentials.password, hashed_password=db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect Password")
    access_token = Oauth2.create_access_token(data={"user_id": db_user.id})

    return {"access_token": access_token, "token_type": "bearer"}


