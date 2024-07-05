from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from schemas.common import QueryRequest
from services.common import query_llm

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/llm/query")
def req_llm_query(body: QueryRequest):
    query = body.query
    return query_llm(query)
