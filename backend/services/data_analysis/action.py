from logging import getLogger

from sqlalchemy.orm import Session

from database.crud import metadata as metadata_crud

from .mermaid import MermaidERD

logger = getLogger("uvicorn.app")


def generate_erd_for_datasource(db: Session, data_source_id: int, user_id: int) -> list[str]:
    logger.debug("Generating ERD for data source: %s", data_source_id)
    database_information_list = metadata_crud.get_database_information(db, data_source_id, user_id)
    erds = []
    for database_information in database_information_list:
        logger.info("Generating ERD for database: %s", database_information.database_name)
        erd = MermaidERD(title=database_information.database_name)
        for table_information in database_information.table_information:
            logger.info("Generating ERD for table: %s", table_information.table_name)
            table_name = table_information.table_name
            table_info = table_information.table_info
            columns = table_info.get("columns")
            columns_attributes = []
            for column in columns:
                column_name = column.get("column_name")
                # replace all white spaces with bar because mermaid does not support white spaces
                columns_attributes.append({"column_name": column_name, "column_type": column["column_type"]})
                if "referenced_table_name" in column:
                    erd.add_relationship(table_name, column["referenced_table_name"], "contains")
            erd.add_entity(table_name, columns_attributes)

            logger.info("Generating ERD for table: %s", table_name)
            logger.info("Table information: %s", table_info)
        erds.append(erd.generate_code())
    return erds
