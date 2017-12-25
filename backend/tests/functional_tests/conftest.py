"""Module for global fixtures that may be useful during application testing."""
from typing import Any

import pytest
from starbase import Connection

from medtagger.config import AppConfiguration
from medtagger.database import Base, engine, session
from medtagger.database.fixtures import insert_scan_categories
from medtagger.clients.hbase_client import HBaseClient


@pytest.fixture
def prepare_environment() -> Any:
    """Prepare environment for testing purpose (setup DBs, fixtures) and clean up after the tests."""
    print('Getting needed entries')
    configuration = AppConfiguration()
    host = configuration.get('hbase', 'host', fallback='localhost')
    port = configuration.getint('hbase', 'rest_port', fallback=8080)

    print('Preparing databases.')
    Base.metadata.create_all(engine)
    hbase_connection = Connection(host=host, port=port)
    for table_name in HBaseClient.HBASE_SCHEMA:
        list_of_columns = HBaseClient.HBASE_SCHEMA[table_name]
        table = hbase_connection.table(table_name)
        table.create(*list_of_columns)

    print('Applying fixtures')
    insert_scan_categories()

    # Run the test
    yield

    print('Removing all data.')
    session.close_all()
    Base.metadata.drop_all(engine)
    for table_name in HBaseClient.HBASE_SCHEMA:
        list_of_columns = HBaseClient.HBASE_SCHEMA[table_name]
        table = hbase_connection.table(table_name)
        table.drop()


@pytest.fixture
def synchronous_celery(mocker: Any) -> Any:
    """Set Celery to executing tasks eagerly (each time tasks are called/delayed)."""
    mocker.patch('medtagger.workers.celery_configuration.task_always_eager', True, create=True)
