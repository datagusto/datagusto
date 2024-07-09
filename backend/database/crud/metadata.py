from typing import Optional

from sqlalchemy.orm import Session

from schemas import metadata as metadata_schema

from .. import models


def create_database_information(db: Session, database_information_create: metadata_schema.DatabaseInformationCreate, user_id: int) -> metadata_schema.DatabaseInformation:
    # convert create class to dict, and create model class from it
    table_information_create_list = database_information_create.table_information
    database_information_create.table_information = []
    new_database_information = models.DatabaseInformation(**database_information_create.dict(), owner_id=user_id)
    new_database_information.table_information = [models.TableInformation(**el.dict(), owner_id=user_id) for el in table_information_create_list]

    db.add(new_database_information)
    db.commit()
    db.refresh(new_database_information)
    return new_database_information


def get_database_information(db: Session, data_source_id: int, user_id: Optional[int]) -> list[metadata_schema.DatabaseInformation]:
    if user_id:
        database_information = db.query(models.DatabaseInformation).filter(
            models.DatabaseInformation.data_source_id == data_source_id,
            models.DatabaseInformation.owner_id == user_id,
        ).all()
        return [metadata_schema.DatabaseInformation.from_orm(database) for database in database_information]
    database_information = db.query(models.DatabaseInformation).filter(
        models.DatabaseInformation.data_source_id == data_source_id,
    ).all()
    return [metadata_schema.DatabaseInformation.from_orm(database) for database in database_information]


def delete_database_information(db: Session, data_source_id: int, user_id: int) -> bool:
    database_information = db.query(models.DatabaseInformation).filter(
        models.DatabaseInformation.data_source_id == data_source_id,
        models.DatabaseInformation.owner_id == user_id,
    ).first()
    if database_information:
        db.delete(database_information)
        db.commit()
        return True
    return False


def clear_database_table_information(db: Session):
    db.query(models.DatabaseInformation).delete()
    db.query(models.TableInformation).delete()
    db.commit()
    return True

