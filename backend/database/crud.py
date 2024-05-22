from typing import Optional

from sqlalchemy.orm import Session

from . import models
import schemas


def get_user(db, username: str) -> Optional[schemas.User]:
    user = db.query(models.User).filter(models.User.username == username).first()
    return schemas.User(**user.__dict__) if user else None


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    user_dict = user.dict()
    password = user_dict.pop('password')
    new_user = models.User(**user_dict, password_hash=schemas.User.hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_data_source(db: Session, data_source_id: int, user_id: Optional[int]) -> schemas.DataSource:
    if user_id:
        data_source = db.query(models.DataSource).filter(
            models.DataSource.id == data_source_id,
            models.DataSource.owner_id == user_id
        ).first()
        return schemas.DataSource.from_orm(data_source) if data_source else None
    data_source = db.query(models.DataSource).filter(models.DataSource.id == data_source_id).first()
    return schemas.DataSource.from_orm(data_source) if data_source else None


def get_data_sources(db: Session, user_id: Optional[int], skip: int = 0, limit: int = 100) -> list[schemas.DataSource]:
    if user_id:
        data_sources = db.query(models.DataSource).filter(
            models.DataSource.owner_id == user_id
        ).offset(skip).limit(limit).all()
        return [schemas.DataSource.from_orm(data_source) for data_source in data_sources]
    data_sources = db.query(models.DataSource).offset(skip).limit(limit).all()
    return [schemas.DataSource.from_orm(data_source) for data_source in data_sources]


def create_data_source(db: Session, data_source: schemas.DataSourceCreate, user_id: int) -> schemas.DataSource:
    new_data_source = models.DataSource(**data_source.dict(), owner_id=user_id)
    db.add(new_data_source)
    db.commit()
    db.refresh(new_data_source)
    return new_data_source


def create_database_information(db: Session, database_information_create: schemas.DatabaseInformationCreate, user_id: int) -> schemas.DatabaseInformation:
    # convert create class to dict, and create model class from it
    table_information_create_list = database_information_create.table_information
    database_information_create.table_information = []
    new_database_information = models.DatabaseInformation(**database_information_create.dict(), owner_id=user_id)
    new_database_information.table_information = [models.TableInformation(**el.dict(), owner_id=user_id) for el in table_information_create_list]

    db.add(new_database_information)
    db.commit()
    db.refresh(new_database_information)
    return new_database_information


def get_database_information(db: Session, data_source_id: int, user_id: Optional[int]) -> list[schemas.DatabaseInformation]:
    if user_id:
        database_information = db.query(models.DatabaseInformation).filter(
            models.DatabaseInformation.data_source_id == data_source_id,
            models.DatabaseInformation.owner_id == user_id
        ).all()
        return [schemas.DatabaseInformation.from_orm(database) for database in database_information]
    database_information = db.query(models.DatabaseInformation).filter(
        models.DatabaseInformation.data_source_id == data_source_id
    ).all()
    return [schemas.DatabaseInformation.from_orm(database) for database in database_information]


def clear_database_table_information(db: Session):
    db.query(models.DatabaseInformation).delete()
    db.query(models.TableInformation).delete()
    db.commit()
    return True


def get_table(db: Session, data_source_id: int, table_name: str, user_id: Optional[int]) -> Optional[schemas.TableInformation]:
    if user_id:
        table = db.query(models.TableInformation).filter(
            models.TableInformation.database_id == data_source_id,
            models.TableInformation.table_name == table_name,
            models.TableInformation.owner_id == user_id
        ).first()
        return schemas.TableInformation.from_orm(table) if table else None
    table = db.query(models.TableInformation).filter(
        models.TableInformation.database_id == data_source_id,
        models.TableInformation.table_name == table_name
    ).first()
    return schemas.TableInformation.from_orm(table) if table else None


# def get_tables(db: Session) -> list[str]:
#     return db.query(models.DatabaseInformation.data_source_id, models.DatabaseInformation.table_name).distinct().all()
# not using
# def get_columns_in_table(db: Session, data_source_id: int, table_name: str) -> list[schemas.DatabaseInformation]:
#     return db.query(models.DatabaseInformation).filter(models.DatabaseInformation.data_source_id == data_source_id, models.DatabaseInformation.table_name == table_name).all()
# def create_database_column_information_bulk(db: Session, database_column_information: list[schemas.DatabaseInformationCreate]) -> list[schemas.DatabaseInformation]:
#     new_database_column_information = [models.DatabaseInformation(**el.dict()) for el in database_column_information]
#     db.add_all(new_database_column_information)
#     db.commit()
#     return new_database_column_information
# def get_todo_by_title(db: Session, tiitle: str):
#     return db.query(models.Todo).filter(models.Todo.tiitle == tiitle).first()
