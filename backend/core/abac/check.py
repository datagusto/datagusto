from operator import and_, or_

from sqlalchemy.orm import Session

from database import models
from database.models import ResourceAccess
from .types import PermissionType


def check_access(db: Session, user_id: int, data_source_id: int, action: PermissionType) -> bool:
    # TODO: For now we are only checking access for data sources
    user = db.query(models.User).filter(models.User.id == user_id).first()
    data_source = db.query(models.DataSource).filter(models.DataSource.id == data_source_id).first()

    # if user is the owner of the data source
    if data_source.owner_id == user_id:
        return True

    # if user is not owner, but it is shared with the user
    access = db.query(ResourceAccess).filter(
        and_(
            ResourceAccess.user_id == user_id,
            ResourceAccess.resource_id == data_source_id,
            ResourceAccess.permission == action
        ),
    ).first()
    if access:
        return True

    # resource is shared cases
    # case 1: shared with everyone (user_id and tenant_id is None)
    # case 2: shared with everyone in the tenant (user_id None, and tenant_id is int)
    access = db.query(ResourceAccess).filter(
        and_(
            ResourceAccess.user_id.is_(None),
            or_(
                ResourceAccess.tenant_id.is_(None),
                ResourceAccess.tenant_id == user.tenant_id,
            ),
            ResourceAccess.resource_id == data_source_id,
            ResourceAccess.permission == action
        ),
    ).first()
    if access:
        return True

    return False


def get_accessible_resource_ids(db: Session, user_id: int) -> list[int]:
    user = db.query(models.User).filter(models.User.id == user_id).one()

    # shared with the user
    shared_permissions = db.query(models.ResourceAccess.resource_id).filter(
        and_(
            models.ResourceAccess.user_id == user_id,
            models.ResourceAccess.tenant_id.is_(None)
        )
    )

    # shared with everyone
    public_shared_permissions = db.query(models.ResourceAccess.resource_id).filter(
        and_(
            models.ResourceAccess.user_id.is_(None),
            models.ResourceAccess.tenant_id.is_(None)
        )
    )

    # shared with all users in the user's tenant
    tenant_shared_resources = db.query(models.ResourceAccess.resource_id).filter(
        and_(
            models.ResourceAccess.user_id.is_(None),
            models.ResourceAccess.tenant_id == user.tenant_id
        )
    )

    # Combine the queries using union
    # accessible_resources = own_resources.union(shared_resources, tenant_shared_resources).all()
    shared_permissions = shared_permissions.union(public_shared_permissions, tenant_shared_resources).all()

    return [permission.resource_id for permission in shared_permissions]
