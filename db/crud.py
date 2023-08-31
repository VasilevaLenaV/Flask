from sqlite3 import IntegrityError

from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return None


def create_user(db: Session, user: schemas.UserCreate):
    try:
        hash_pwd = generate_password_hash(user.password)

        db_user = models.User(username=user.username, email=user.email, hashed_password=hash_pwd)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user, None
    except IntegrityError as e:
        return None, e


def update_user(db: Session, user_id: int, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None
