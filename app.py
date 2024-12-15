"""Взаимодействие с базой данных"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User, Post

def create_user(db: Session, username: str, email: str, password: str):
    """добавляет в таблицу Users несколько записей со значениями полей username, email и password"""
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id,
            "username": user.username,
            "email": user.email}

def get_users(db: Session):
    """извлекает все записи из таблицы Users"""
    users = db.query(User).all()
    return [{"id": u.id,
             "username": u.username,
             "email": u.email} for u in users]

def update_user(db: Session, user_id: int, email: str):
    """обновляет поле email у одного из пользователей"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.email = email
    db.commit()
    db.refresh(user)
    return {"id": user.id,
            "username": user.username,
            "email": user.email}

def delete_user(db: Session, user_id: int):
    """удаляет пользователя и все его посты"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Post).filter(Post.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

def create_post(db: Session, title: str, content: str, user_id: int):
    """добавляет в таблицу Posts несколько записей, связанных с пользователями из таблицы Users"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id}

def read_posts(db: Session):
    """извлекает все записи из таблицы Users"""
    posts = db.query(Post).all()
    return [{"id": p.id,
             "title": p.title,
             "content": p.content,
             "user_id": p.user_id} for p in posts]

def update_post(db: Session, post_id: int, content: str):
    """обновляет поле content у одного из постов"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.content = content
    db.commit()
    db.refresh(post)
    return {"id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id}

def delete_post(db: Session, post_id: int):
    """удаляет один из постов"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
