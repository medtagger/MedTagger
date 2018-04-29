"""Module responsible for defining ORM layer."""
from datetime import datetime
from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, func, MetaData, Column, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

from medtagger.config import AppConfiguration


class MedTaggerBase(object):  # pylint: disable=too-few-public-methods
    """Base class for all of the models."""

    _created = Column(DateTime, nullable=False, server_default=func.now(), default=datetime.utcnow)
    _modified = Column(DateTime, nullable=False, server_default=func.now(), default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        """Return string representation."""
        return '<{}: {}>'.format(self.__class__.__name__, getattr(self, 'id', '-'))

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

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(cls=MedTaggerBase, metadata=metadata)
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
