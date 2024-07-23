from logging import getLogger

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from core.vector_db_adapter.factory import VectorDatabaseFactory
from database.crud import data_source as data_source_crud
from dependencies import get_current_user, get_db
from schemas import data_source as data_source_schema
from schemas.user import User
from services.data_source.action import (
    create_data_source,
    create_data_source_from_file,
    delete_data_source_by_id,
    get_sample_data_from_table,
    test_data_source_connection,
)
from services.metadata.action import delete_metadata

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.get("/", response_model=list[data_source_schema.DataSource])
def req_get_data_sources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[data_source_schema.DataSource]:
    data_sources = data_source_crud.get_data_sources(db, skip=skip, limit=limit, user_id=current_user.id)
    return data_sources


@router.get("/{data_source_id}", response_model=data_source_schema.DataSource)
def req_get_data_source_by_id(
    data_source_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> data_source_schema.DataSource:
    data_source = data_source_crud.get_data_source(db, data_source_id=data_source_id, user_id=current_user.id)
    return data_source


@router.get("/{data_source_id}/table_name/{table_name}")
def req_get_columns_in_table(
    data_source_id: int,
    table_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    df = get_sample_data_from_table(db, data_source_id, table_name, current_user.id)
    response = {"data": df.to_json(orient="records")}
    return response


@router.post("/test_connection", response_model=dict[str, bool])
def req_test_data_source_connection(data_source: data_source_schema.DataSourceCreate) -> dict[str, bool]:
    result = test_data_source_connection(data_source)
    return {"result": result}


@router.post("/", response_model=data_source_schema.DataSource, status_code=status.HTTP_201_CREATED)
def req_create_data_source(
    data_source: data_source_schema.DataSourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> data_source_schema.DataSource:
    return create_data_source(db, data_source, current_user.id)


@router.delete("/{data_source_id}")
def req_delete_data_source_by_id(
    data_source_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    # delete metadata
    logger.info("Deleting metadata for data source: %s", data_source_id)
    delete_metadata(db, data_source_id, current_user.id)
    # delete vectors
    factory = VectorDatabaseFactory()
    vector_db_client = factory.get_vector_database()
    logger.info("Deleting vectors for data source: %s", data_source_id)
    try:
        vector_db_client.delete_by_filter({"data_source_id": data_source_id})
    except Exception:
        logger.warning("Failed to delete vectors for data source: %s", data_source_id)
        pass
    vector_db_client_join = factory.get_vector_database_join()
    try:
        vector_db_client_join.delete_by_filter({"data_source_id": data_source_id})
    except Exception:
        logger.warning("Failed to delete vectors for data source: %s", data_source_id)
        pass

    delete_data_source_by_id(db, data_source_id, current_user.id)
    return {"message": "Data source deleted successfully"}


@router.post("/file/", response_model=data_source_schema.DataSource)
def req_create_data_source_from_file(
    detail: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> data_source_schema.DataSource:
    return create_data_source_from_file(db, detail, file.file, file.filename, current_user.id)
