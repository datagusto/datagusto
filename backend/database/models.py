from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.abac.types import PermissionType, ResourceType
from core.data_source_adapter.types import DataSourceType
from database.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    tenant_id = Column("tenant_id", Integer, nullable=True)
    username = Column("username", String(50), unique=True, nullable=False)
    password_hash = Column("password_hash", String(100), nullable=False)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class DataSource(Base):
    __tablename__ = "data_source"
    id = Column("id", Integer, primary_key=True)
    owner_id = Column("owner_id", Integer, ForeignKey("user.id"))
    tenant_id = Column("tenant_id", Integer, nullable=True)
    name = Column("name", String(100))
    type = Column("type", Enum(DataSourceType))
    description = Column("description", String(1000))
    connection = Column("connection", JSON)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class ResourceAccess(Base):
    __tablename__ = "resource_access"
    id = Column("id", Integer, primary_key=True)
    owner_id = Column("owner_id", Integer, ForeignKey("user.id"))
    user_id = Column("user_id", Integer, ForeignKey("user.id"), nullable=True, default=None)
    tenant_id = Column("tenant_id", Integer, nullable=True, default=None)
    resource_id = Column("resource_id", Integer, ForeignKey("data_source.id"))
    resource_type = Column("resource_type", Enum(ResourceType))
    permission = Column("permission", Enum(PermissionType))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class DatabaseInformation(Base):
    __tablename__ = "database_information"
    id = Column("id", Integer, primary_key=True)
    owner_id = Column("owner_id", Integer, ForeignKey("user.id"))
    data_source_id = Column("data_source_id", Integer, ForeignKey("data_source.id"))
    database_name = Column("database_name", String(100))
    schema_name = Column("schema_name", String(100))
    table_information = relationship(
        "TableInformation",
        back_populates="database_information",
        cascade="all, delete-orphan",
    )
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class TableInformation(Base):
    __tablename__ = "table_information"
    id = Column("id", Integer, primary_key=True)
    owner_id = Column("owner_id", Integer, ForeignKey("user.id"))
    data_source_id = Column("data_source_id", Integer, ForeignKey("data_source.id"))
    database_id = Column("database_id", Integer, ForeignKey("database_information.id"))
    database_information = relationship("DatabaseInformation", back_populates="table_information")
    table_name = Column("table_name", String(100))
    table_info = Column("table_info", JSON)
    deleted_at = Column(DateTime, default=None, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
