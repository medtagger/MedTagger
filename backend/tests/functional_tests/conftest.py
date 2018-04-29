"""Module for global fixtures that may be useful during application testing."""
import logging
from typing import Any

import pytest

from medtagger.api import InvalidArgumentsException
from medtagger.api.rest import app
from medtagger.database import Base, session
from medtagger.database.fixtures import apply_all_fixtures
from medtagger.clients.hbase_client import HBaseClient
from medtagger.api.auth.business import create_user, sign_in_user
from medtagger.api.users.business import set_user_role
from medtagger.repositories.label_tag import LabelTagRepository
from medtagger.repositories.roles import RolesRepository
from medtagger.repositories.scan_categories import ScanCategoriesRepository

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
        for key in HBaseClient().get_all_keys(table_name):
            HBaseClient().delete(table_name, key)


@pytest.fixture
def synchronous_celery(mocker: Any) -> Any:
    """Set Celery to executing tasks eagerly (each time tasks are called/delayed)."""
    mocker.patch('medtagger.workers.celery_configuration.task_always_eager', True, create=True)


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
    user_id = create_user(email, password, first_name, last_name)
    set_user_role(user_id, role.name)

    with app.app_context():
        return sign_in_user(email, password)


def create_tag_and_assign_to_category(key: str, name: str, scan_category_key: str) -> str:
    """Create Label Tag and assign it to Scan Category.

    :param key: key that will identify such Label Tag
    :param name: name that will be used in the User Interface for such Label Tag
    :param scan_category_key: key of the Scan Category that Label Tag will be assigned to
    :return: Label Tag key
    """
    label_tag = LabelTagRepository.add_new_tag(key, name)
    ScanCategoriesRepository.assign_label_tag(label_tag, scan_category_key)
    return label_tag.key
