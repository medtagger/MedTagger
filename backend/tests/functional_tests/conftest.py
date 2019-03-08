"""Module for global fixtures that may be useful during application testing."""
import logging
from typing import Any

import pytest
from cassandra.cqlengine.models import ModelMetaClass

from medtagger import storage
from medtagger.api import InvalidArgumentsException
from medtagger.api.auth.business import create_user, sign_in_user
from medtagger.api.rest import app
from medtagger.api.users.business import set_user_role
from medtagger.database import Base, Session, db_transaction_session
from medtagger.database.fixtures import apply_all_fixtures
from medtagger.repositories import roles as RolesRepository
from medtagger.storage import models

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def prepare_environment() -> Any:
    """Prepare environment for testing purpose (setup DBs, fixtures) and clean up after the tests."""
    logger.info('Applying fixtures to PostgreSQL.')
    apply_all_fixtures()

    # Run the test
    yield

    logger.info('Clearing databases.')
    _clear_databases()


@pytest.fixture
def synchronous_celery(mocker: Any) -> Any:
    """Set Celery to executing tasks eagerly (each time tasks are called/delayed)."""
    mocker.patch('medtagger.workers.celery_configuration.task_always_eager', True, create=True)


def pytest_keyboard_interrupt(excinfo: Any) -> None:
    """Clear database after tests that were interrupted with keyboard."""
    logger.error('Tests interrupted!')
    logger.info('Clearing databases.')
    _clear_databases()


def get_token_for_logged_in_user(role: str) -> str:
    """Create and log in user with given role and return its token.

    :param: role that will be granted to created user
    :return: user token
    """
    logger.info('Preparing user with admin role.')

    email = 'admin@medtagger.com'
    password = 'medtagger2'
    first_name = 'First'
    last_name = 'Last'

    role = RolesRepository.get_role_with_name(role)
    if role is None:
        raise InvalidArgumentsException('Role does not exist.')
    user_id, _ = create_user(email, password, first_name, last_name)
    set_user_role(user_id, role.name)

    with app.app_context():
        return sign_in_user(email, password)


def _clear_databases() -> None:
    logger.info('Removing all data from PostgreSQL.')
    with db_transaction_session() as sess:
        for table in reversed(Base.metadata.sorted_tables):
            sess.execute('TRUNCATE TABLE "{}" RESTART IDENTITY CASCADE;'.format(table.name))
    Session.close_all()

    logger.info('Removing all data from Cassandra.')
    storage_session = storage.create_session()
    storage_session.set_keyspace(storage.MEDTAGGER_KEYSPACE)
    for model_name in dir(models):
        model = getattr(models, model_name)
        if issubclass(model.__class__, ModelMetaClass) and model.__table_name__:
            storage_session.execute('TRUNCATE {}'.format(model.__table_name__))
