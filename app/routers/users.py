
from fastapi import APIRouter, Depends, Response, status, HTTPException, APIRouter

from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import utils 
from typing import List, Optional

router = APIRouter( )

@router.post("/",status_code= status.HTTP_201_CREATED,response_model=schemas.User)
async def create_user(user: schemas.UserCreate,  db:Session = Depends(get_db)):
    user.hashed_password = utils.get_password_hash(user.hashed_password)
    new_user = models.User( **user.dict())
    print(new_user)
    print("Look here")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.User)
async def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
    return user


@router.get("/",response_model=List[schemas.User])
async def get_users(db:Session = Depends(get_db)):
    return db.query(models.User).all()
