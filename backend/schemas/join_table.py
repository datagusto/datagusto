from pydantic import BaseModel


class JoinableTableIndexingCreate(BaseModel):
    data_source_id: int


class JoinableTableJoinData(BaseModel):
    data_source_id: int
    table_name: str
