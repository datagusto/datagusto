from logging import getLogger

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(dotenv_path=".env")

from dependencies import get_current_user  # noqa E402
from endpoints import analysis, common, data_sources, joinable, matching, metadata, user, resource_access  # noqa E402

logger = getLogger("uvicorn.app")

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
def exception_handler(request: Request, exc: Exception) -> tuple[dict[str, str], int]:
    logger.exception(exc)
    return {
        "message": "Internal Server Error",
        "detail": str(exc),
    }, 200


app.include_router(common.router, prefix="/common")
app.include_router(user.router, prefix="/user")
app.include_router(data_sources.router, prefix="/data_sources", dependencies=[Depends(get_current_user)])
app.include_router(metadata.router, prefix="/metadata", dependencies=[Depends(get_current_user)])
app.include_router(joinable.router, prefix="/joinable", dependencies=[Depends(get_current_user)])
app.include_router(matching.router, prefix="/matching", dependencies=[Depends(get_current_user)])
app.include_router(analysis.router, prefix="/analysis", dependencies=[Depends(get_current_user)])
app.include_router(resource_access.router, prefix="/resource_access", dependencies=[Depends(get_current_user)])
