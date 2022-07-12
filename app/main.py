

from fastapi import Body, Depends, FastAPI

from app.routers import posts, users, auth, votes
from fastapi.middleware.cors import CORSMiddleware


import app.models as models
from app.database import  engine

#we dont need this now, since we are using alembic
#models.Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/login", tags=["Auth"])
app.include_router(votes.router, prefix="/votes", tags=["Votes"])
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