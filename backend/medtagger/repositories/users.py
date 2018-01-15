"""Module responsible for definition of Users' Repository."""
from typing import List, Optional

from medtagger.database import db_session
from medtagger.database.models import User
from medtagger.types import UserInfo


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
    def get_all_users() -> List[UserInfo]:
        """Return list of all users."""
        with db_session() as session:
            users = session.query(User).order_by(User.id).all()
        user_info = list(map(UsersRepository.user_to_user_info, users))
        return user_info

    @staticmethod
    def get_user_with_email(user_email: str) -> Optional[User]:
        """Get user with given email.

        :return Optional of User"""
        with db_session() as session:
            user = session.query(User).filter(User.email == user_email).first()
        return user

    @staticmethod
    def get_user_with_id(user_id: int) -> Optional[User]:
        """Get user with given email.

        :return Optional of User"""
        with db_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def user_to_user_info(user: User) -> UserInfo:
        """Map user entity to UserInfo tuple."""
        role = user.roles[0].name
        return UserInfo(id=user.id,
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        role=role)
