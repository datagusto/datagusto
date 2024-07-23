from logging import getLogger
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.abac.types import PermissionType
from database.crud.data_source import get_data_source
from database.crud.resource_access import (
    create_resource_access,
    delete_resource_access,
    delete_resource_access_by_resource_id,
    get_resource_access_by_access_user,
)
from dependencies import get_current_user, get_db
from schemas import resource_access as resource_access_schema
from schemas.user import User

router = APIRouter()
logger = getLogger("uvicorn.app")


@router.get("/tenant_shared/{data_source_id}")
def req_get_tenant_shared_mode(
    data_source_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, Optional[str]]:
    data_source = get_data_source(db, data_source_id=data_source_id, user_id=current_user.id)
    access = get_resource_access_by_access_user(
        db,
        None,
        current_user.tenant_id,
        data_source_id,
        action=[PermissionType.Read, PermissionType.Write],
    )
    permission = None
    if data_source.owner_id == current_user.id:
        if access:
            permission = "owner"
        # permission = PermissionType.Write
    if permission is None:
        # check if resource is shared in the tenant
        permission = access.permission if access else permission
    return {"permission": permission}


@router.post("/", response_model=resource_access_schema.ResourceAccess, status_code=status.HTTP_201_CREATED)
def req_create_resource_access(
    resource_access: resource_access_schema.ResourceAccessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> resource_access_schema.ResourceAccess:
    logger.info("Creating access policy: %s", resource_access.dict())
    return create_resource_access(db, resource_access, current_user.id)


@router.delete("/{resource_access_id}", response_model=resource_access_schema.ResourceAccess)
def req_delete_resource_access(
    resource_access_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> resource_access_schema.ResourceAccess:
    logger.info("Deleting resource access policy %s for user: %s", resource_access_id, current_user.username)
    resource_access = delete_resource_access(db, current_user.id, resource_access_id)
    return resource_access


@router.delete("/resource_id/{resource_id}", response_model=resource_access_schema.ResourceAccess)
def req_delete_resource_access_by_resource_id(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> resource_access_schema.ResourceAccess:
    logger.info("Deleting resource access policy for resource_id: %s", resource_id)
    resource_access = delete_resource_access_by_resource_id(db, current_user.id, resource_id)
    return resource_access
