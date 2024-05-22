from logging import getLogger

from fastapi import HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from adapters.connections import get_connection
from database import crud
from .sub import generate_text_from_data, flatten_concatenation
from ..vectordb.load import storage_client_join

logger = getLogger("uvicorn.app")
SCORE_THRESHOLD = 0.07


def join_data(data_source_id: int, table_name: str, db: Session, threshold: float = SCORE_THRESHOLD):
    # get data from target data source
    data_source = crud.get_data_source(db, data_source_id=data_source_id)
    if not data_source:
        logger.warning("data_source_id: %s not found", data_source_id)
        raise HTTPException(status_code=404, detail=f"DataSource ID: {data_source_id} not found")

    # create connection to data source
    connection = get_connection(data_source)

    # get columns in the data source
    table_information = crud.get_table(db, data_source_id, table_name)
    joinable_columns = []
    for column in table_information.table_info["columns"]:
        logger.info("data_source_id: %s, table_name: %s, column_name: %s, column_type: %s",
                    data_source_id, table_name, column["column_name"], column["column_type"])
        # skip unsupported column types
        # TODO: check with the white list of supported column types instead of black list
        if column["column_type"].startswith(
                ("timestamp", "geometry", "year", "decimal", "enum", "set", "datetime", "blob")):
            continue

        data = connection.select_column(table_name, column["column_name"], limit=1000)
        data = flatten_concatenation(data)

        query = generate_text_from_data(table_name, column["column_name"], data)

        filter = {"column_type": column["column_type"]}
        result = storage_client_join.query_with_filter(query, filter, top_k=5)
        for doc, score in result:
            metadata = doc.metadata
            if (metadata["data_source_id"] == data_source_id
                    and metadata["table_name"] == table_name
                    and metadata["column_name"] == column["column_name"]):
                continue
            logger.info("doc: %s, score: %s", doc.metadata, score)

            if score > threshold:
                continue

            # delete soon
            if column["column_name"] == "id" and metadata["column_name"] == "customer_id":
                continue

            joinable_columns.append({
                "source_column_name": column["column_name"],
                "target_data_source_id": metadata["data_source_id"],
                "target_table_name": metadata["table_name"],
                "target_column_name": metadata["column_name"],
                "score": score,
            })

    # aggregate the joinable_info
    joinable_info = {}
    for c in joinable_columns:
        source_column_name = c["source_column_name"]
        target_data_source_id = c["target_data_source_id"]
        target_table_name = c["target_table_name"]
        target_column_name = c["target_column_name"]

        joinable_info.setdefault(target_data_source_id, {}).setdefault(target_table_name, []).append(
            [source_column_name, target_column_name])

    # load data
    source_data_columns = [col["column_name"] for col in table_information.table_info.get("columns")]
    source_data_data = connection.select_table(table_name, limit=1000)
    logger.info("source_data_data: %s", source_data_data[:5])
    logger.info("source_data_columns: %s", source_data_columns)
    merged_df = pd.DataFrame(source_data_data, columns=source_data_columns)

    for target_data_source_id in joinable_info:
        target_data_source = crud.get_data_source(db, data_source_id=target_data_source_id)
        target_connection = get_connection(target_data_source)
        for target_table_name in joinable_info[target_data_source_id]:
            target_table_information = crud.get_table(db, target_data_source_id, target_table_name)
            target_data_columns = [col["column_name"] for col in target_table_information.table_info.get("columns")]
            target_data_data = target_connection.select_table(target_table_name, limit=1000)

            target_data_df = pd.DataFrame(target_data_data, columns=target_data_columns)

            left_on, right_on = zip(*joinable_info[target_data_source_id][target_table_name])

            merged_df = pd.merge(merged_df, target_data_df, how="left", left_on=left_on, right_on=right_on)

    return merged_df, joinable_info
