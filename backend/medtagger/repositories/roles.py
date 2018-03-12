"""Module responsible for definition of Roles' Repository."""
from typing import List

from sqlalchemy.orm.exc import NoResultFound

from medtagger.api import InvalidArgumentsException
from medtagger.database import db_session
from medtagger.database.models import Role
from medtagger.repositories.users import UsersRepository


class RolesRepository(object):
    """Repository for Roles."""

    @staticmethod
    def get_all_roles() -> List[Role]:
        """Get all available roles."""
        return Role.query.all()

    @staticmethod
    def get_role_with_name(role_name: str) -> Role:
        """Get role with given name."""
        role = Role.query.filter(Role.name == role_name).one()
        return role

    @staticmethod
    def set_user_role(user_id: int, role_name: str) -> None:
        """Set user's role. Old role will be replaced."""
        try:
            user = UsersRepository.get_user_by_id(user_id)
        except NoResultFound:
            raise InvalidArgumentsException('User with this id does not exist.')
        try:
            role = RolesRepository.get_role_with_name(role_name)
        except NoResultFound:
            raise InvalidArgumentsException('Role with this name does not exist.')
        with db_session() as session:
            user.roles = [role]
            session.add(user)
