"""Lab 9"""

from typing import List
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from app import (
    create_user, get_users, update_user, delete_user,
    create_post, read_posts, update_post, delete_post
)

engine = create_engine("sqlite:///test.db")

Base.metadata.create_all(bind=engine)
session = sessionmaker(autoflush=False, bind=engine)
db = session()

app = FastAPI()

@app.post("/users/", response_model=dict)
def add_user(username: str, email: str, password: str):
    return create_user(db, username, email, password)

@app.get("/users/", response_model=List[dict])
def list_users():
    return get_users(db)

@app.put("/users/{user_id}", response_model=dict)
def modify_user(user_id: int, email: str):
    return update_user(db, user_id, email)

@app.delete("/users/{user_id}", response_model=dict)
def remove_user(user_id: int):
    return delete_user(db, user_id)

@app.post("/posts/", response_model=dict)
def add_post(title: str, content: str, user_id: int):
    return create_post(db, title, content, user_id)

@app.get("/posts/", response_model=List[dict])
def list_posts():
    return read_posts(db)

@app.put("/posts/{post_id}", response_model=dict)
def modify_post(post_id: int, content: str):
    return update_post(db, post_id, content)

@app.delete("/posts/{post_id}", response_model=dict)
def remove_post(post_id: int):
    return delete_post(db, post_id)
