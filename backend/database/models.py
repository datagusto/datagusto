from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON

from database.database import Base
from adapters.types import DataSourceType


class DataSource(Base):
    __tablename__ = 'data_source'
    id = Column('id', Integer, primary_key=True)
    owner_id = Column('owner_id', String(50))
    name = Column('name', String(100))
    type = Column('type', Enum(DataSourceType))
    description = Column('description', String(1000))
    connection = Column('connection', JSON)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class DatabaseColumnInformation(Base):
    __tablename__ = 'database_column_information'
    id = Column('id', Integer, primary_key=True)
    data_source_id = Column('data_source_id', Integer)
    database_name = Column('database_name', String(100))
    table_name = Column('table_name', String(100))
    column_name = Column('column_name', String(100))
    column_info = Column('column_info', JSON)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
