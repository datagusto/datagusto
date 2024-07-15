from operator import and_, or_
from typing import Optional

from sqlalchemy.orm import Session

from core.abac.check import check_access, get_accessible_resource_ids
from core.abac.types import PermissionType
from schemas import data_source as data_source_schema
from schemas import metadata as metadata_schema

from .. import models


def get_data_source(db: Session, data_source_id: int, user_id: int) -> data_source_schema.DataSource:
    if check_access(db, user_id, data_source_id, PermissionType.Read) is False:
        raise Exception("Access Denied")

    data_source = (
        db.query(models.DataSource)
        .filter(
            and_(
                models.DataSource.id == data_source_id,
                models.DataSource.owner_id == user_id,
            ),
        )
        .first()
    )
    return data_source_schema.DataSource.from_orm(data_source) if data_source else None


def get_data_sources(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[data_source_schema.DataSource]:
    accessible_resource_ids = get_accessible_resource_ids(db, user_id)
    data_sources = (
        db.query(models.DataSource)
        .filter(or_(models.DataSource.owner_id == user_id, models.DataSource.id.in_(accessible_resource_ids)))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [data_source_schema.DataSource.from_orm(data_source) for data_source in data_sources]


def create_data_source(
    db: Session,
    data_source: data_source_schema.DataSourceCreate,
    user_id: int,
) -> data_source_schema.DataSource:
    new_data_source = models.DataSource(**data_source.dict(), owner_id=user_id)
    db.add(new_data_source)
    db.commit()
    db.refresh(new_data_source)
    return new_data_source


def delete_data_source(db: Session, data_source_id: int, user_id: int) -> bool:
    if check_access(db, user_id, data_source_id, PermissionType.Write) is False:
        raise Exception("Access Denied")
    data_source = (
        db.query(models.DataSource)
        .filter(
            and_(
                models.DataSource.id == data_source_id,
                models.DataSource.owner_id == user_id,
            ),
        )
        .first()
    )
    if data_source:
        db.delete(data_source)
        db.commit()
        return True
    return False


def get_table(
    db: Session,
    data_source_id: int,
    table_name: str,
    user_id: int,
) -> Optional[metadata_schema.TableInformation]:
    if check_access(db, user_id, data_source_id, PermissionType.Read) is False:
        raise Exception("Access Denied")
    table = (
        db.query(models.TableInformation)
        .filter(
            models.TableInformation.data_source_id == data_source_id,
            models.TableInformation.table_name == table_name,
            models.TableInformation.owner_id == user_id,
        )
        .first()
    )
    return metadata_schema.TableInformation.from_orm(table) if table else None
