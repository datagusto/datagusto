from logging import getLogger

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(dotenv_path=".env")

from database import models
from database.database import engine
from dependencies import get_current_user
from endpoints.analysis import router as analysis_router
from endpoints.common import router as common_router
from endpoints.data_sources import router as data_sources_router
from endpoints.joinable import router as joinable_router
from endpoints.matching import router as matching_router
from endpoints.metadata import router as metadata_router
from endpoints.user import router as user_router

logger = getLogger("uvicorn.app")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "*",  # Allow any origin for now
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
def exception_handler(request, exc):
    logger.exception(exc)
    return {
        "message": "Internal Server Error",
        "detail": str(exc)
    }, 200


app.include_router(common_router, prefix="/common")
app.include_router(user_router, prefix="/user")
app.include_router(data_sources_router, prefix="/data_sources", dependencies=[Depends(get_current_user)])
app.include_router(metadata_router, prefix="/metadata", dependencies=[Depends(get_current_user)])
app.include_router(joinable_router, prefix="/joinable", dependencies=[Depends(get_current_user)])
app.include_router(matching_router, prefix="/matching", dependencies=[Depends(get_current_user)])
app.include_router(analysis_router, prefix="/analysis", dependencies=[Depends(get_current_user)])
