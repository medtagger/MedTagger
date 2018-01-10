"""Script for populating dev database with default user accounts."""
import logging

from sqlalchemy import exists
from werkzeug.security import generate_password_hash

from medtagger.database import db_session
from medtagger.database.models import User, Role

logger = logging.getLogger(__name__)


def insert_admin_account() -> None:
    """Insert default admin account."""
    with db_session() as session:
        user_email = 'admin@medtagger.com'
        user_exists = session.query(exists().where(User.email == user_email)).scalar()
        if user_exists:
            logger.warning('Admin user already exists with email "%s"', user_email)
            return
        password = 'medtagger1'
        password_hash = generate_password_hash(password)
        user = User(user_email, password_hash, 'Admin', 'Medtagger')
        role = Role.query.filter_by(name='admin').first()
        user.roles.append(role)
        session.add(user)
        logger.info('User added with email "%s" and password "%s"', user_email, password)


if __name__ == '__main__':
    insert_admin_account()
