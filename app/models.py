from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Author(BaseModel):
    id: str
    name: str
    email: str
    bio: str = ""
    created_at: datetime

class AuthorCreate(BaseModel):
    name: str
    email: str
    bio: str = ""

class Post(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    published: bool = False
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: str
    tags: List[str] = []

class Comment(BaseModel):
    id: str
    post_id: str
    author_name: str
    content: str
    created_at: datetime

class CommentCreate(BaseModel):
    author_name: str
    content: str

class Like(BaseModel):
    id: str
    post_id: str
    user_name: str
    created_at: datetime

class LikeCreate(BaseModel):
    user_name: str

