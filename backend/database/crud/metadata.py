from typing import Optional

from sqlalchemy.orm import Session

from core.abac.check import check_access
from core.abac.types import PermissionType
from schemas import metadata as metadata_schema

from .. import models


def create_database_information(
    db: Session,
    database_information_create: metadata_schema.DatabaseInformationCreate,
    user_id: int,
) -> metadata_schema.DatabaseInformation:
    if check_access(db, user_id, database_information_create.data_source_id, PermissionType.Write) is False:
        raise Exception("Access Denied")
    # convert create class to dict, and create model class from it
    table_information_create_list = database_information_create.table_information
    database_information_create.table_information = []
    new_database_information = models.DatabaseInformation(**database_information_create.dict(), owner_id=user_id)
    new_database_information.table_information = [
        models.TableInformation(**el.dict(), owner_id=user_id) for el in table_information_create_list
    ]

    db.add(new_database_information)
    db.commit()
    db.refresh(new_database_information)
    return new_database_information


def get_database_information(
    db: Session,
    data_source_id: int,
    user_id: Optional[int],
) -> list[metadata_schema.DatabaseInformation]:
    if check_access(db, user_id, data_source_id, PermissionType.Read) is False:
        raise Exception("Access Denied")
    database_information = (
        db.query(models.DatabaseInformation)
        .filter(
            models.DatabaseInformation.data_source_id == data_source_id,
        )
        .all()
    )
    return [metadata_schema.DatabaseInformation.from_orm(database) for database in database_information]


def delete_database_information(db: Session, data_source_id: int, user_id: int) -> bool:
    if check_access(db, user_id, data_source_id, PermissionType.Write) is False:
        raise Exception("Access Denied")
    database_information = (
        db.query(models.DatabaseInformation)
        .filter(
            models.DatabaseInformation.data_source_id == data_source_id,
        )
        .first()
    )
    if database_information:
        db.delete(database_information)
        db.commit()
        return True
    return False


def clear_database_table_information(db: Session) -> bool:
    db.query(models.ResourceAccess).delete()
    db.query(models.TableInformation).delete()
    db.query(models.DatabaseInformation).delete()
    db.commit()
    return True
