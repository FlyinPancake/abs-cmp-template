from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_FILE_ENV = getenv("DATABASE_PATH")
DB_FILE = DB_FILE_ENV if DB_FILE_ENV else "./app_data.sqlite"
SQLALCHEMY_DATABASE_URL = "sqlite:///" + DB_FILE

sqla_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqla_engine)
Base = declarative_base()
