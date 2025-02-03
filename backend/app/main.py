# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Existing user endpoints...

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/author/{author_id}", response_model=List[schemas.Post])
def get_posts_by_author(author_id: int, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.author_id == author_id).all()
    return posts

@app.get("/posts/search/", response_model=List[schemas.Post])
def search_posts_by_title(title: str, db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.title.ilike(f"%{title}%")).all()
    return posts

@app.get("/posts/latest/", response_model=List[schemas.Post])
def get_latest_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).order_by(models.Post.id.desc()).limit(2).all()
    return posts