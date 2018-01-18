"""Module responsible for definition of Roles' Repository."""
from typing import Optional

from medtagger.api import InvalidArgumentsException
from medtagger.database import db_session
from medtagger.database.models import Role
from medtagger.repositories.users import UsersRepository


class RolesRepository(object):
    """Repository for Roles."""

    @staticmethod
    def get_role_with_name(role_name: str) -> Optional[Role]:
        """Get role with given name.

        :return Optional of role"""
        with db_session() as session:
            role = session.query(Role).filter(Role.name == role_name).first()
        return role

    @staticmethod
    def set_user_role(user_id: int, role_name: str) -> None:
        """Set user's role. Old role is being replaced."""
        user = UsersRepository.get_user_by_id(user_id)
        if user is None:
            raise InvalidArgumentsException("User with this id does not exist.")
        role = RolesRepository.get_role_with_name(role_name)
        if role is None:
            raise InvalidArgumentsException("Role with this name does not exist.")
        with db_session() as session:
            user.roles.clear()
            user.roles.append(role)
            session.add(user)
