from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class User(UserBase):
    id: int
    password_hash: Optional[str] = None
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def hash_password(cls, password):
        return pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    class Config:
        from_attributes = True
