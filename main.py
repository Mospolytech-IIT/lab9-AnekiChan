"""Lab 9"""

from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, HTTPException, Form
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from models import User, Post
from app import (
    create_user, get_users, update_user, delete_user,
    create_post, read_posts, update_post, delete_post
)

engine = create_engine("sqlite:///test.db")

Base.metadata.create_all(bind=engine)
session = sessionmaker(autoflush=False, bind=engine)
db = session()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def main_page(request: Request):
    """Главная страница"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users/", response_model=List[dict])
def list_users(request: Request):
    """Список пользователй"""
    users = get_users(db)
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

@app.get("/users/create")
def create_user_page(request: Request):
    """Форма для создания пользователя"""
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/users/", response_model=dict)
def add_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Создание пользователя"""
    return create_user(db, username, email, password)

@app.get("/users/{user_id}/edit")
def edit_user_page(request: Request, user_id: int):
    """Форма лоя редактирования пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.put("/users/{user_id}", response_model=dict)
def modify_user(user_id: int, email: str = Form(...)):
    """Редатирование пользователя"""
    return update_user(db, user_id, email)

@app.delete("/users/{user_id}", response_model=dict)
def remove_user(user_id: int):
    """Удаление пользователя"""
    return delete_user(db, user_id)

@app.get("/posts/", response_model=List[dict])
def list_posts(request: Request):
    """Список постов"""
    posts = read_posts(db)
    return templates.TemplateResponse("posts_list.html", {"request": request, "posts": posts})

@app.get("/posts/create")
def create_post_page(request: Request):
    """Форма для создания поста"""
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/", response_model=dict)
def add_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    """Создание поста"""
    return create_post(db, title, content, user_id)

@app.get("/posts/{post_id}/edit")
def edit_post_page(request: Request, post_id: int):
    """Форма для редактирования поста"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})

@app.put("/posts/{post_id}", response_model=dict)
def modify_post(post_id: int, content: str = Form(...)):
    """Редакирование поста"""
    return update_post(db, post_id, content)

@app.delete("/posts/{post_id}", response_model=dict)
def remove_post(post_id: int):
    """Удаление пооста"""
    return delete_post(db, post_id)
