"""Module responsible for defining ORM layer."""
import os
from datetime import datetime
from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event, exc, func, MetaData, Column, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from medtagger.config import AppConfiguration


class MedTaggerBase:  # pylint: disable=too-few-public-methods
    """Base class for all of the models."""

    _created = Column(DateTime, nullable=False, server_default=func.now(), default=datetime.utcnow)
    _modified = Column(DateTime, nullable=False, server_default=func.now(), default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        """Return string representation."""
        return '<{}: {}>'.format(self.__class__.__name__, getattr(self, 'id', '-'))

    def save(self) -> None:
        """Save the model into the database after changes."""
        with db_transaction_session() as _session:
            _session.add(self)


configuration = AppConfiguration()
db_uri = configuration.get('db', 'database_uri')
db_pool_size = configuration.getint('db', 'connection_pool_size')
engine = create_engine(db_uri, pool_size=db_pool_size, pool_recycle=1800, convert_unicode=True, pool_pre_ping=True)
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


@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    connection_record.info['pid'] = os.getpid()


@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(f"Connection record belongs to PID {connection_record.info['pid']}, "
                                     f"attempting to check out in PID {pid}")


def is_alive() -> bool:
    """Return boolean information if database is alive or not."""
    try:
        session.execute('SELECT 1')
        return True
    except Exception:  # pylint: disable=broad-except
        return False


@contextmanager
def db_connection_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    yield session


@contextmanager
def db_transaction_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
