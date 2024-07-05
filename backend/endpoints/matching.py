from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from schemas import matching_table as matching_schema
from services.data_matching.action import find_schema_matching, find_data_matching

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/find_schema_matching/", response_model=matching_schema.SchemaMatchingResult)
def req_find_schema_matching(target_file: UploadFile = File(...), source_file: UploadFile = File(...), ) -> dict:
    response = find_schema_matching(target_file.filename, target_file.file, source_file.filename, source_file.file)
    return response


@router.post("/find_data_matching/")
def post_find_data_matching(matching: str = Form(...), target_file: UploadFile = File(...),
                            source_file: UploadFile = File(...)):
    response_buffer = find_data_matching(target_file.file, source_file.file, matching)

    # CSVファイルをストリーミングレスポンスとして返す
    response = StreamingResponse(iter([response_buffer.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    return response
