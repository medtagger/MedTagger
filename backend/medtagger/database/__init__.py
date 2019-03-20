"""Module responsible for defining ORM layer."""
import os
from datetime import datetime
from typing import Any, Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event, exc, func, orm, MetaData, Column, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
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
db_pool_recycle = configuration.getint('db', 'connection_pool_recycle')
engine = create_engine(db_uri, pool_size=db_pool_size, pool_recycle=db_pool_recycle,
                       convert_unicode=True, pool_pre_ping=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(cls=MedTaggerBase, metadata=metadata)
Base.query = Session.query_property()


@event.listens_for(engine, "connect")
def connect(dbapi_connection: Any, connection_record: Any) -> None:
    """Save current PID where connection has been set up for future comparison."""
    # pylint: disable=unused-argument  # Needs to follow SQLAlchemy interface
    connection_record.info['pid'] = os.getpid()


@event.listens_for(engine, "checkout")
def checkout(dbapi_connection: Any, connection_record: Any, connection_proxy: Any) -> None:
    """Checkout is called each time a connection is retrieved from the Connection Pool.

    To be sure that our code did not fork in the meanwhile, let's double check the PID.
    In case of mismatch, it is necessary to create new connection to the SQL DB by disconnecting
    from current session and start again.
    """
    # pylint: disable=unused-argument  # Needs to follow SQLAlchemy interface
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(f'Connection record belongs to PID {connection_record.info["pid"]}, '
                                     f'attempting to check out in PID {pid}')


def is_alive() -> bool:
    """Return boolean information if database is alive or not."""
    try:
        Session.execute('SELECT 1')
        return True
    except Exception:  # pylint: disable=broad-except
        return False


@contextmanager
def db_connection_session() -> Generator[orm.Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    Session()
    yield Session


@contextmanager
def db_transaction_session() -> Generator[orm.Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    Session()
    try:
        yield Session
        Session.commit()
    except Exception:
        Session.rollback()
        raise
