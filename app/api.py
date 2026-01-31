from fastapi import FastAPI, HTTPException
from typing import List, Optional
from app.models import Author, AuthorCreate, Post, PostCreate, Comment, CommentCreate
from app.storage import authors, posts, comments
from app.utils import gen_id, now

app = FastAPI()

# authors

@app.get("/authors")
def list_authors():
    return list(authors.values())

@app.post("/authors")
def create_author(data: AuthorCreate):
    a = Author(
        id=gen_id(),
        name=data.name,
        email=data.email,
        bio=data.bio,
        created_at=now()
    )
    authors[a.id] = a
    return a

@app.get("/authors/{author_id}")
def get_author(author_id: str):
    if author_id not in authors:
        raise HTTPException(404)
    return authors[author_id]

# posts

@app.get("/posts")
def list_posts(published_only: bool = True, tag: Optional[str] = None):
    p = list(posts.values())
    if published_only:
        p = [x for x in p if x.published]
    if tag:
        p = [x for x in p if tag in x.tags]
    return p

@app.get("/posts/{post_id}")
def get_post(post_id: str):
    if post_id not in posts:
        raise HTTPException(404)
    return posts[post_id]

@app.post("/posts")
def create_post(data: PostCreate):
    if data.author_id not in authors:
        raise HTTPException(400, "author not found")
    p = Post(
        id=gen_id(),
        title=data.title,
        content=data.content,
        author_id=data.author_id,
        tags=data.tags,
        created_at=now(),
        updated_at=now()
    )
    posts[p.id] = p
    return p

@app.post("/posts/{post_id}/publish")
def publish_post(post_id: str):
    if post_id not in posts:
        raise HTTPException(404)
    posts[post_id].published = True
    return posts[post_id]

# comments

@app.get("/posts/{post_id}/comments")
def list_comments(post_id: str):
    if post_id not in posts:
        raise HTTPException(404)
    return [c for c in comments.values() if c.post_id == post_id]

@app.post("/posts/{post_id}/comments")
def create_comment(post_id: str, data: CommentCreate):
    if post_id not in posts:
        raise HTTPException(404)
    c = Comment(
        id=gen_id(),
        post_id=post_id,
        author_name=data.author_name,
        content=data.content,
        created_at=now()
    )
    comments[c.id] = c
    return c

# NEW FEATURE NEEDED:
# The product team wants to add a "likes" feature for posts
# Requirements:
# - Users should be able to like a post
# - Each post should track total like count
# - Need endpoint: POST /posts/{post_id}/like
# - Need endpoint: GET /posts/{post_id}/likes (return count)
# - Optional: prevent duplicate likes from same user (by name)

