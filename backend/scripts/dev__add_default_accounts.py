"""Script for populating dev database with default user accounts."""
import logging
import logging.config

from sqlalchemy import exists

from medtagger.api.security import hash_password
from medtagger.database import db_session
from medtagger.database.models import User, Role

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def insert_admin_account() -> None:
    """Insert default admin account."""
    user_email = 'admin@medtagger.com'
    password = 'medtagger1'
    password_hash = hash_password(password)

    with db_session() as session:
        user_exists = session.query(exists().where(User.email == user_email)).scalar()
        if user_exists:
            logger.warning('Admin user already exists with email "%s"', user_email)
            return

        role = Role.query.filter_by(name='admin').first()
        if not role:
            logger.error('Role not found! You have probably forgot to apply fixtures.')
            return

        user = User(user_email, password_hash, 'Admin', 'Medtagger')
        user.roles.append(role)
        session.add(user)
    logger.info('User added with email "%s" and password "%s"', user_email, password)


if __name__ == '__main__':
    try:
        insert_admin_account()
    except Exception:  # pylint: disable=broad-except;  This should be fixed once we move to repository
        logger.exception('Unhandled exception while inserting default admin account!')
