from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from schemas import metadata as metadata_schema
from schemas.user import User
from services.joinable_table.offline import indexing
from services.metadata.action import get_and_save_metadata, query_metadata, delete_all_metadata

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/")
def req_get_metadata(model: metadata_schema.GetMetadata,
                              current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    get_and_save_metadata(db, model.data_source_id, current_user.id)
    # create joinable table index
    logger.info("Create joinable data index: %s", model.data_source_id)
    indexing(model.data_source_id, current_user.id, db)
    return {"message": "Getting metadata completed."}


@router.get("/query/")
def req_query_metadata(query: str, current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    response = query_metadata(db, query, current_user.id)
    return response


@router.delete("/clear-all")
def delete_vector_db(db: Session = Depends(get_db)):
    # this is for testing purpose
    delete_all_metadata(db)
    return {"message": "Database and VectorDB are cleared."}
