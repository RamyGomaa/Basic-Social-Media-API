import datetime
from email.policy import default
from time import timezone
from sqlalchemy import TIMESTAMP, Boolean, Column, Date, ForeignKey, Integer, String, null, text
from sqlalchemy.orm import relationship

from .database import Base as base

Base = base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone =True), nullable=False, server_default=text('now()'))
    posts = relationship("Post", back_populates="owner")
    votes = relationship("Vote", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True)
    content = Column(String, index=False)
    published = Column(Boolean, server_default= 'TRUE',nullable = False)
    created_at = Column(TIMESTAMP(timezone =True), nullable=False, server_default=text('now()'))

    owner = relationship("User", back_populates="posts")
    votes = relationship("Vote", back_populates="post")

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)
    
    user  = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")