"""Insert all database fixtures."""
import logging.config
from typing import List, cast

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from medtagger.database import db_session
from medtagger.definitions import LabelTool
from medtagger.database.models import ScanCategory, Role, LabelTag

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

ROLES = ['admin', 'doctor', 'volunteer']


def insert_user_roles() -> None:
    """Insert default user Roles."""
    with db_session() as session:
        for role_name in ROLES:
            role_exists = session.query(exists().where(Role.name == role_name)).scalar()
            if role_exists:
                logger.info('Role exists with name "%s"', role_name)
                continue

            role = Role(name=role_name)
            session.add(role)
            logger.info('Role added for name "%s"', role_name)


def apply_all_fixtures() -> None:
    """Apply all available fixtures."""
    logger.info('Applying fixtures for user Roles...')
    insert_user_roles()


if __name__ == '__main__':
    try:
        apply_all_fixtures()
    except IntegrityError:
        logger.exception('An error occurred while applying fixtures! It is highly possible that there was'
                         'a race condition between multiple processes applying fixtures at the same time.')
