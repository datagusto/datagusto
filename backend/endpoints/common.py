from logging import getLogger

from fastapi import APIRouter

from schemas.common import QueryRequest
from services.common import query_llm

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/llm/query")
def req_llm_query(body: QueryRequest) -> str:
    query = body.query
    return query_llm(query)
