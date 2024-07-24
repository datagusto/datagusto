from logging import getLogger

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_current_user, get_db
from schemas import join_table as join_schema
from schemas.user import User
from services.joinable_table.offline import indexing
from services.joinable_table.online import join_data

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/indexing/")
def post_joinable_table_indexing(
    body: join_schema.JoinableTableIndexingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    data_source_id = body.data_source_id
    logger.info("Indexing data source: %s", data_source_id)

    indexing(data_source_id, current_user.id, db)

    return {"message": "Joinable data index created."}


@router.post("/join_data/")
def post_joinable_table_join_data(
    body: join_schema.JoinableTableJoinData,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, dict[int, dict]]:
    logger.info("Joining data")
    data_source_id = body.data_source_id
    table_name = body.table_name
    merged_dfs = join_data(data_source_id, current_user.id, table_name, db)
    for target_data_source_id, tables in merged_dfs.items():
        for table_name, info in tables.items():
            logger.info(f"Target data source: {target_data_source_id}, table: {table_name}")
            # Convert DataFrame to JSON
            info["data"] = info["data"].to_json(orient="records")

    response_body = {"data": merged_dfs}

    return response_body
