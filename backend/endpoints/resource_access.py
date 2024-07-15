from logging import getLogger

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.crud.resource_access import create_resource_access, delete_resource_access
from dependencies import get_current_user, get_db
from schemas.user import User
from schemas import resource_access as resource_access_schema

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.post("/", response_model=resource_access_schema.ResourceAccess, status_code=status.HTTP_201_CREATED)
def req_create_resource_access(
    resource_access: resource_access_schema.ResourceAccessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> resource_access_schema.ResourceAccess:
    logger.info("Creating access policy: %s", resource_access.dict())
    return create_resource_access(db, resource_access)


@router.delete("/{resource_access_id}", response_model=resource_access_schema.ResourceAccess)
def req_delete_resource_access(
    resource_access_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> resource_access_schema.ResourceAccess:
    logger.info("Deleting resource access policy %s for user: %s", resource_access_id, current_user.username)
    resource_access = delete_resource_access(db, current_user.id, resource_access_id)
    return resource_access
