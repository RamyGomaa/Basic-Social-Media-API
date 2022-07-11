from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool]= True
    class Config:
        orm_mode = True
    
class PostUpdate(PostBase):
    id:int  
    
class PostCreate(PostBase):
    pass
        
class UserBase(BaseModel):
    email:EmailStr
    
    class Config:
        orm_mode = True

class UserOut(UserBase):
    id : int
    
class Post(PostBase):
    id:int  
    created_at: datetime
    owner:UserOut
    
class UserCreate(UserBase):
    hashed_password :str
    
class UserLogin(UserBase):
    password :str
    
class User(UserBase):
    id : int
    created_at : datetime
    posts: List[Post] = []
    



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None