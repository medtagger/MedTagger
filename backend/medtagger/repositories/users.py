"""Module responsible for definition of UsersRepository."""
from typing import List, Optional

from medtagger.database import db_transaction_session
from medtagger.database.models import User


def add_new_user(new_user: User) -> int:
    """Add new user.

    :return: id of the new user
    """
    with db_transaction_session() as session:
        session.add(new_user)
    return new_user.id


def get_all_users() -> List[User]:
    """Return list of all users."""
    return User.query.order_by(User.id).all()


def get_user_by_email(user_email: str) -> Optional[User]:
    """Get user with given email.

    :return Optional of User
    """
    return User.query.filter(User.email == user_email).first()


def get_user_by_id(user_id: int) -> User:
    """Get user with given id."""
    return User.query.filter(User.id == user_id).one()


def set_user_info(user: User, first_name: str, last_name: str) -> None:
    """Set user's info."""
    with db_transaction_session() as session:
        user.first_name = first_name
        user.last_name = last_name
        session.add(user)


def set_user_settings(user: User, name: str, value: object) -> None:
    """Set user's settings parameter of specified name to provided value."""
    with db_transaction_session() as session:
        setattr(user.settings, name, value)
        session.add(user.settings)
