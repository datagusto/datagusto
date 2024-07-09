
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class GetMetadata(BaseModel):
    data_source_id: int


class TableInformationBase(BaseModel):
    data_source_id: int
    table_name: str
    table_info: dict


class TableInformationCreate(TableInformationBase):
    pass


class TableInformation(TableInformationBase):
    id: int
    owner_id: int
    database_id: int
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DatabaseInformationBase(BaseModel):
    data_source_id: int
    database_name: str
    schema_name: str


class DatabaseInformation(DatabaseInformationBase):
    id: int
    owner_id: int
    table_information: List[TableInformation] = []
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DatabaseInformationCreate(DatabaseInformationBase):
    table_information: List[TableInformationCreate] = []
    pass
