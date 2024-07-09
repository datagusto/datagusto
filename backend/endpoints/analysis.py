from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from schemas.user import User
from services.data_analysis.action import generate_erd_for_datasource

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/erd/{data_source_id}")
def req_generate_erd_for_data_source(data_source_id: int, current_user: User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    result = generate_erd_for_datasource(db, data_source_id, current_user.id)
    return {"erds": result}
