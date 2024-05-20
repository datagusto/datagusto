import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USAGE = os.getenv("DATABASE_USAGE", "POSTGRESQL")

# connect args for sqlite connection
connect_args = {}
if DATABASE_USAGE == "POSTGRESQL":
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:password@localhost/postgres")
elif DATABASE_USAGE == "SQLITE3":
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///./db/database.db")
    connect_args = {"check_same_thread": False}
else:
    raise Exception("DATABASE_USAGE is not configured properly. Please check DATABASE_USAGE in .env file")

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=connect_args, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
