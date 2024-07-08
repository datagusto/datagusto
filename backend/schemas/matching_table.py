from typing import List

from pydantic import BaseModel


class SchemaMatchingResult(BaseModel):
    target_data_columns: List[str]
    target_data_matched_columns: List[str]
    source_data_columns: List[str]
    source_data_matched_columns: List[str]
    matching: dict
