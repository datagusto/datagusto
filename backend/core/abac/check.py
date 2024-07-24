import itertools

from sqlalchemy.orm import Session

from database import models
from database.crud.resource_access import (
    get_resource_access_by_access_user,
    get_resource_access_list,
)

from .types import PermissionType


def check_access(db: Session, user_id: int, data_source_id: int, action: PermissionType) -> bool:
    # TODO: For now we are only checking access for data sources
    user = db.query(models.User).filter(models.User.id == user_id).first()
    data_source = db.query(models.DataSource).filter(models.DataSource.id == data_source_id).first()

    # if user is the owner of the data source
    if data_source.owner_id == user_id:
        return True

    # if user is not owner, but it is shared with the user
    access = get_resource_access_by_access_user(db, user_id, None, data_source_id, action=action)
    if access:
        return True

    # resource is shared cases
    # case 1: shared with everyone (user_id and tenant_id is None)
    shared_all_access = get_resource_access_by_access_user(db, None, None, data_source_id, action=action)
    # case 2: shared with everyone in the tenant (user_id None, and tenant_id is int)
    shared_tenant_access = get_resource_access_by_access_user(db, None, user.tenant_id, data_source_id, action=action)
    if shared_all_access or shared_tenant_access:
        return True

    return False


def get_accessible_resource_ids(db: Session, user_id: int) -> list[int]:
    user = db.query(models.User).filter(models.User.id == user_id).one()

    # shared with the user
    shared_permissions = get_resource_access_list(db, user_id, None)

    # shared with everyone
    public_shared_permissions = get_resource_access_list(db, None, None)
    # shared with all users in the user's tenant
    tenant_shared_resources = get_resource_access_list(db, None, user.tenant_id)

    # Combine the queries using union
    accessible_resources = itertools.chain(shared_permissions, public_shared_permissions, tenant_shared_resources)

    resource_ids = [permission.resource_id for permission in accessible_resources]

    return list(dict.fromkeys(resource_ids))
