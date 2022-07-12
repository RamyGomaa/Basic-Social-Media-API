from fastapi import FastAPI, Response,status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from typing import Optional
import app.models as models, app.schemas as schemas, app.Oauth2 as Oauth2
from app.database import get_db


router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(get_db),current_user:schemas.User = Depends(Oauth2.get_current_user)):
    #checking for the existance of the post
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
    
    #checking for if the user votes on his own post.
    if post.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cannot vote on your own post")
    
    
    db_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    db_vote = db_query.first()
    if db_vote:
            db.delete(db_vote)
            db.commit()


            return Response(status_code=status.HTTP_200_OK, content="message: Vote deleted")

    else:
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id,)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote
    
    
    # vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    # fountVote = vote_query.first()
    # if vote.dir == 1:
       
    #     if fountVote:
    #         raise HTTPException(status.HTTP_409_CONFLICT, detail="User already voted")
        
    #     newVote = models.Vote(user_id=current_user.id,post_id=vote.post_id)
    #     db.add(newVote)
    #     db.commit()
    #     db.refresh(newVote)
    #     return {
    #         "message": "Vote created",
    #         "data": newVote
    #     }
    # else:
    #     if not fountVote:
    #          raise HTTPException(status.HTTP_409_CONFLICT, detail="User hasn't voted")
    #     vote_query.delete(synchronize_session=False)
    #     db.commit()
    #     return {"message": "vote deleted successfully"}