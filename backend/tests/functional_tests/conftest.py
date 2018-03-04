"""Module for global fixtures that may be useful during application testing."""
import logging
from typing import Any

import pytest

from medtagger.database import Base, session
from medtagger.database.fixtures import apply_all_fixtures
from medtagger.clients.hbase_client import HBaseClient

logger = logging.getLogger(__name__)


@pytest.fixture
def prepare_environment() -> Any:
    """Prepare environment for testing purpose (setup DBs, fixtures) and clean up after the tests."""
    logger.info('Applying fixtures to PostgreSQL.')
    apply_all_fixtures()

    # Run the test
    yield

    logger.info('Removing all data from PostgreSQL.')
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close_all()

    logger.info('Removing all data from HBase.')
    for table_name in HBaseClient.HBASE_SCHEMA:
        for key in HBaseClient.get_all_keys(table_name):
            HBaseClient.delete(table_name, key)


@pytest.fixture
def synchronous_celery(mocker: Any) -> Any:
    """Set Celery to executing tasks eagerly (each time tasks are called/delayed)."""
    mocker.patch('medtagger.workers.celery_configuration.task_always_eager', True, create=True)
