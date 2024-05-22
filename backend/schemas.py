from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from adapters.types import DataSourceType


class DataSourceBase(BaseModel):
    owner_id: int
    name: str
    type: DataSourceType
    description: Optional[str] = None
    connection: dict


class DataSourceCreate(DataSourceBase):
    pass


class DataSource(DataSourceBase):
    id: int
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DataSourceGetMetadata(BaseModel):
    data_source_id: int


class TableInformationBase(BaseModel):
    table_name: str
    table_info: dict


class TableInformationCreate(TableInformationBase):
    pass


class TableInformation(TableInformationBase):
    id: int
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DatabaseInformationBase(BaseModel):
    data_source_id: int
    database_name: str
    schema_name: str


class DatabaseInformation(DatabaseInformationBase):
    id: int
    table_information: List[TableInformation] = []
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class DatabaseInformationCreate(DatabaseInformationBase):
    table_information: List[TableInformationCreate] = []
    pass


class JoinableTableIndexingCreate(BaseModel):
    data_source_id: int


class JoinableTableJoinData(BaseModel):
    data_source_id: int
    table_name: str


class SchemaMatchingResult(BaseModel):
    target_data_columns: List[str]
    target_data_matched_columns: List[str]
    source_data_columns: List[str]
    source_data_matched_columns: List[str]
    matching: dict
