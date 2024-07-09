from fastapi import Depends
from sqlalchemy.orm import Session

from core.auth import oauth2_scheme, verify_access_token
from database.database import SessionLocal
from schemas.user import User


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = verify_access_token(token, db)
    return user
