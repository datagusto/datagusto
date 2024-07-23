import enum


class ResourceType(str, enum.Enum):
    # user: user resource
    User = "user"
    # data_source: data source resource
    DataSource = "data_source"
    # metadata: metadata resource
    Metadata = "metadata"


class PermissionType(str, enum.Enum):
    # read: user can read the data
    Read = "read"
    # write: user can read/write the data
    Write = "write"
