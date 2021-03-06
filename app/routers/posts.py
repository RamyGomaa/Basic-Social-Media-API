
from fastapi import APIRouter, Depends, Response, status, HTTPException, APIRouter
from sqlalchemy import func

from sqlalchemy.orm import Session
from app.database import get_db
import app.models as models
import app.schemas as schemas
from typing import List, Optional
import app.Oauth2 as Oauth2

router = APIRouter()

@router.get("/",response_model=List[schemas.PostFull])
async def getPosts(db:Session = Depends(get_db),limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts= db.query(models.Post, func.count(models.Vote.post_id).label("voteCount")).join(models.Vote, models.Post.id == models.Vote.post_id,  isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}",response_model=schemas.Post)
async def getPost(id:int, response:Response, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
    return post

@router.post("/",status_code= status.HTTP_201_CREATED,response_model=schemas.Post)
async def createPost(post: schemas.PostCreate,  db:Session = Depends(get_db),current_user:schemas.User = Depends(Oauth2.get_current_user)):
   
    new_post = models.Post( **post.dict() , owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

       
@router.put("/{id}",response_model=schemas.Post)
async def update_post(updated_post: schemas.PostUpdate, current_user:schemas.User = Depends(Oauth2.get_current_user), db:Session = Depends(get_db)):
    
    
    db_query = db.query(models.Post).filter(models.Post.id == updated_post.id)
    db_post = db_query.first()
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have permission to update this post")
    db_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return db_query.first()

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, db:Session = Depends(get_db),current_user:schemas.User = Depends(Oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You dont have permission to delete this post")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

