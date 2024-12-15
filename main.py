"""Lab 9"""

from typing import List
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

engine = create_engine("sqlite:///test.db")

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")

Base.metadata.create_all(bind=engine)
session = sessionmaker(autoflush=False, bind=engine)
db = session()

app = FastAPI()

@app.post("/users/", response_model=dict)
def create_user(username: str, email: str, password: str):
    """добавляет в таблицу Users несколько записей со значениями полей username, email и password"""
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id,
            "username": user.username, 
            "email": user.email}

@app.get("/users/", response_model=List[dict])
def read_users():
    """извлекает все записи из таблицы Users"""
    users = db.query(User).all()
    return [{"id": u.id,
             "username": u.username, 
             "email": u.email} for u in users]

@app.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, email: str):
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

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    """удаляет пользователя и все его посты"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(Post).filter(Post.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": "User and all their posts deleted"}

@app.post("/posts/", response_model=dict)
def create_post(title: str, content: str, user_id: int):
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

@app.get("/posts/", response_model=List[dict])
def read_posts():
    """извлекает все записи из таблицы Users"""
    posts = db.query(Post).all()
    return [{"id": p.id,
             "title": p.title, 
             "content": p.content, 
             "user_id": p.user_id} for p in posts]

@app.put("/posts/{post_id}", response_model=dict)
def update_post(post_id: int, content: str):
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

@app.delete("/posts/{post_id}", response_model=dict)
def delete_post(post_id: int):
    """удаляет один из постов"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
