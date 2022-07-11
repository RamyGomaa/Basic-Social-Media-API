from tokenize import String
from typing import List, Optional
from fastapi import Body, Depends, FastAPI,Response, status, HTTPException,APIRouter
from pydantic import BaseModel
from routers import posts, users, auth


import utils 
import models, schemas
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/login", tags=["Auth"])
@app.get("/")
async def root():
    return {"status": "200"}



















#not used but can be used later for refereneces 
"""
#list of posts
posts = [ {   "title": "Post1 Title",
            "content": "Post1 Body",
            "id": 1,
    },
          {    
            "title": "Post2 Title",
            "content": "Post2 Body",
            "id":2
            }  
     ]

# get a post from posts list by id.
def getPostById(id:int):
    for post in posts:
        if post["id"] == id:
            return post

#delete a post from posts list
def delete_post_by_id(id:int):
    for post in posts:
        if post["id"] == id:
            posts.remove(post)
            return post

def update_post_by_id(id:int, sentPost:schemas.Post):
    for i,post in enumerate(posts):
        if post["id"] == id:
            newPost = sentPost.dict()
            newPost["id"] = id
            posts[i]  = newPost
            return newPost
"""