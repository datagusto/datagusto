from typing import Optional

from sqlalchemy.orm import Session

from schemas import user as user_schema

from .. import models


def get_user(db, username: str) -> Optional[user_schema.User]:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user_schema.User(**user.__dict__) if user else None


def create_user(db: Session, user: user_schema.UserCreate) -> user_schema.User:
    user_dict = user.dict()
    password = user_dict.pop('password')
    new_user = models.User(**user_dict, password_hash=user_schema.User.hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
