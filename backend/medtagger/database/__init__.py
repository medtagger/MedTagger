"""Module responsible for defining ORM layer."""
from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

from medtagger.config import AppConfiguration


class DataLabelingBase(object):  # pylint: disable=too-few-public-methods
    """Base class for all of the models."""

    def save(self) -> None:
        """Save the model into the database after changes."""
        with db_session() as _session:
            _session.add(self)


db = SQLAlchemy()

configuration = AppConfiguration()
db_uri = configuration.get('db', 'database_uri')
db_pool_size = configuration.getint('db', 'connection_pool_size')
engine = create_engine(db_uri, pool_size=db_pool_size, convert_unicode=True)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base(cls=DataLabelingBase)
Base.query = session.query_property()


def is_alive() -> bool:
    """Return boolean information if database is alive or not."""
    try:
        session.execute('SELECT 1')
        return True
    except Exception:  # pylint: disable=broad-except
        return False


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
