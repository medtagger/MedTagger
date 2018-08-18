"""Insert all database fixtures."""
import logging.config

from sqlalchemy.exc import IntegrityError

from medtagger.repositories import roles as RolesRepository

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

ROLES = ['admin', 'doctor', 'volunteer']


def insert_user_roles() -> None:
    """Insert default user Roles."""
    for role_name in ROLES:
        if RolesRepository.role_exists(role_name):
            logger.info('Role exists with name "%s"', role_name)
            continue

        RolesRepository.add_role(role_name)
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
