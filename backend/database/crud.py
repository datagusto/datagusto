from sqlalchemy.orm import Session

from . import models
import schemas


def get_data_source(db: Session, data_source_id: int) -> schemas.DataSource:
    return db.query(models.DataSource).filter(models.DataSource.id == data_source_id).first()


# def get_todo_by_title(db: Session, tiitle: str):
#     return db.query(models.Todo).filter(models.Todo.tiitle == tiitle).first()


def get_data_sources(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.DataSource]:
    return db.query(models.DataSource).offset(skip).limit(limit).all()


def create_data_source(db: Session, data_source: schemas.DataSourceCreate) -> schemas.DataSource:
    new_data_source = models.DataSource(**data_source.dict())
    db.add(new_data_source)
    db.commit()
    db.refresh(new_data_source)
    return new_data_source


def create_database_column_information_bulk(db: Session, database_column_information: list[schemas.DatabaseInformationCreate]) -> list[schemas.DatabaseInformation]:
    new_database_column_information = [models.DatabaseColumnInformation(**el.dict()) for el in database_column_information]
    db.add_all(new_database_column_information)
    db.commit()
    return new_database_column_information


def clear_database_column_information(db: Session):
    db.query(models.DatabaseColumnInformation).delete()
    db.commit()
    return True


def get_columns_in_data_source(db: Session, data_source_id: int) -> list[schemas.DatabaseInformation]:
    return db.query(models.DatabaseColumnInformation).filter(models.DatabaseColumnInformation.data_source_id == data_source_id).all()


def get_tables(db: Session) -> list[str]:
    return db.query(models.DatabaseColumnInformation.data_source_id, models.DatabaseColumnInformation.table_name).distinct().all()


def get_columns_in_table(db: Session, data_source_id: int, table_name: str) -> list[schemas.DatabaseInformation]:
    return db.query(models.DatabaseColumnInformation).filter(models.DatabaseColumnInformation.data_source_id == data_source_id, models.DatabaseColumnInformation.table_name == table_name).all()
