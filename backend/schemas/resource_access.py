from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from core.abac.types import PermissionType, ResourceType


class ResourceAccessBase(BaseModel):
    owner_id: int
    user_id: Optional[int] = None
    tenant_id: Optional[int] = None
    resource_id: int
    resource_type: ResourceType = ResourceType.DataSource
    permission: PermissionType = PermissionType.Read


class ResourceAccessCreate(ResourceAccessBase):
    pass


class ResourceAccess(ResourceAccessBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
