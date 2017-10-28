"""Module responsible for business logic for user management"""
from flask_user import UserManager

from data_labeling.database import db_session
from data_labeling.database.models import User

user_manager = UserManager()


def create_user(username: str, password: str) -> int:
    """Create user with the given user information. Password is being hashed.
    :return: id of the new user
    """
    password_hash = user_manager.hash_password(password)
    new_user = User(username, password_hash)
    with db_session() as session:
        session.add(new_user)
    return new_user.id
