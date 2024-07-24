from typing import Dict, Optional, Union

from sqlalchemy.orm import Query, Session

from core.abac.types import PermissionType, ResourceType
from schemas import resource_access as resource_access_schema

from .. import models


def get_filtered_resource_access_query(db: Session, filters: Dict[str, Optional[int]]) -> Query:
    query = db.query(models.ResourceAccess)
    for key, value in filters.items():
        if value is None:
            query = query.filter(getattr(models.ResourceAccess, key).is_(value))
        elif isinstance(value, list):
            query = query.filter(getattr(models.ResourceAccess, key).in_(value))
        else:
            query = query.filter(getattr(models.ResourceAccess, key) == value)
    return query


def get_resource_access_by_owner_id(
    db: Session,
    owner_id: int,
    resource_id: int,
    resource_type: ResourceType = ResourceType.DataSource,
    action: Union[PermissionType, list[PermissionType]] = PermissionType.Read,
) -> Optional[resource_access_schema.ResourceAccess]:
    filters = {"owner_id": owner_id, "resource_id": resource_id, "resource_type": resource_type, "permission": action}
    resource_access = get_filtered_resource_access_query(db, filters).first()
    return resource_access_schema.ResourceAccess.from_orm(resource_access) if resource_access else None


def get_resource_access_list(
    db: Session,
    user_id: Optional[int],
    tenant_id: Optional[int],
    resource_type: ResourceType = ResourceType.DataSource,
) -> list[resource_access_schema.ResourceAccess]:
    filters = {"user_id": user_id, "tenant_id": tenant_id, "resource_type": resource_type}
    resource_access = get_filtered_resource_access_query(db, filters).all()
    return [resource_access_schema.ResourceAccess.from_orm(access) for access in resource_access]


def get_resource_access_by_access_user(
    db: Session,
    user_id: Optional[int],
    tenant_id: Optional[int],
    resource_id: int,
    resource_type: ResourceType = ResourceType.DataSource,
    action: PermissionType = PermissionType.Read,
) -> Optional[resource_access_schema.ResourceAccess]:
    filters = {
        "user_id": user_id,
        "tenant_id": tenant_id,
        "resource_id": resource_id,
        "resource_type": resource_type,
        "permission": action,
    }
    resource_access = get_filtered_resource_access_query(db, filters).first()
    return resource_access_schema.ResourceAccess.from_orm(resource_access) if resource_access else None


def create_resource_access(
    db: Session,
    resource_access: resource_access_schema.ResourceAccessCreate,
    owner_id: int,
) -> resource_access_schema.ResourceAccess:
    new_resource_access = models.ResourceAccess(**resource_access.dict(), owner_id=owner_id)
    db.add(new_resource_access)
    db.commit()
    db.refresh(new_resource_access)
    return new_resource_access


def delete_resource_access(
    db: Session,
    owner_id: int,
    id: int,
    resource_type: ResourceType = ResourceType.DataSource,
    permission: PermissionType = PermissionType.Read,
) -> Optional[resource_access_schema.ResourceAccess]:
    filters = {"owner_id": owner_id, "id": id, "resource_type": resource_type, "permission": permission}
    resource_access = get_filtered_resource_access_query(db, filters).first()
    if resource_access:
        db.delete(resource_access)
        db.commit()
        return resource_access_schema.ResourceAccess.from_orm(resource_access)
    return None


def delete_resource_access_by_resource_id(
    db: Session,
    owner_id: int,
    resource_id: int,
    resource_type: ResourceType = ResourceType.DataSource,
    permission: PermissionType = PermissionType.Read,
) -> Optional[resource_access_schema.ResourceAccess]:
    filters = {
        "owner_id": owner_id,
        "resource_id": resource_id,
        "resource_type": resource_type,
        "permission": permission,
    }
    resource_access = get_filtered_resource_access_query(db, filters).first()
    if resource_access:
        db.delete(resource_access)
        db.commit()
        return resource_access_schema.ResourceAccess.from_orm(resource_access)
    return None
