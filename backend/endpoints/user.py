from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.auth import authenticate_user, generate_bearer_token
from database.crud import user as user_crud
from dependencies import get_current_user, get_db
from schemas import user as user_schema

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)) -> user_schema.User:
    _user = user_crud.get_user(db, username=user.username)
    if _user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = user_crud.create_user(db, user)
    return new_user


@router.post("/login", response_model=dict)
def login_for_access_token(user_login: user_schema.UserLogin, db: Session = Depends(get_db)) -> dict:
    user = authenticate_user(db, user_login.username, user_login.password)
    return generate_bearer_token(user.username)


@router.get("/me", response_model=user_schema.UserResponse)
def read_users_me(current_user: user_schema.User = Depends(get_current_user)) -> user_schema.User:
    current_user = get_current_user()
    return current_user
