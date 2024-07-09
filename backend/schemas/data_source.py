from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.data_source_adapter.types import DataSourceType


class DataSourceBase(BaseModel):
    name: str
    type: DataSourceType
    description: Optional[str] = None
    connection: dict


class DataSourceCreate(DataSourceBase):
    pass


class DataSource(DataSourceBase):
    id: int
    owner_id: int
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
