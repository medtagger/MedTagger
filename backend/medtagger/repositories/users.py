"""Module responsible for definition of Users' Repository."""
from typing import List, Optional

from sqlalchemy.orm.exc import NoResultFound

from medtagger.api import InvalidArgumentsException
from medtagger.database import db_session
from medtagger.database.models import User


class UsersRepository(object):
    """Repository for Users."""

    @staticmethod
    def add_new_user(new_user: User) -> int:
        """Add new user.

        :return: id of the new user
        """
        with db_session() as session:
            session.add(new_user)
        return new_user.id

    @staticmethod
    def get_all_users() -> List[User]:
        """Return list of all users."""
        return User.query.order_by(User.id).all()

    @staticmethod
    def get_user_by_email(user_email: str) -> Optional[User]:
        """Get user with given email.

        :return Optional of User
        """
        return User.query.filter(User.email == user_email).first()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Get user with given id."""
        return User.query.filter(User.id == user_id).one()

    @staticmethod
    def set_user_info(user_id: int, firstName: str, lastName: str) -> User:
        """Set user's info."""
        try:
            user = UsersRepository.get_user_by_id(user_id)
        except NoResultFound:
            raise InvalidArgumentsException('User with this id does not exist.')
        with db_session() as session:
            user.first_name = firstName
            user.last_name = lastName
            session.add(user)
