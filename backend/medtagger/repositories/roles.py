"""Module responsible for definition of RolesRepository."""
from typing import List

from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound

from medtagger.api import InvalidArgumentsException
from medtagger.database import db_session
from medtagger.database.models import Role
from medtagger.repositories import users as UsersRepository


def get_all_roles() -> List[Role]:
    """Get all available roles."""
    return Role.query.all()


def get_role_with_name(role_name: str) -> Role:
    """Get role with given name."""
    role = Role.query.filter(Role.name == role_name).one()
    return role


def set_user_role(user_id: int, role_name: str) -> None:
    """Set user's role. Old role will be replaced."""
    try:
        user = UsersRepository.get_user_by_id(user_id)
    except NoResultFound:
        raise InvalidArgumentsException('User with this id does not exist.')
    try:
        role = get_role_with_name(role_name)
    except NoResultFound:
        raise InvalidArgumentsException('Role with this name does not exist.')
    with db_session() as session:
        user.roles = [role]
        session.add(user)


def role_exists(role_name: str) -> bool:
    """Check if such Role with given name exists."""
    with db_session() as session:
        return session.query(exists().where(Role.name == role_name)).scalar()


def add_role(role_name: str) -> Role:
    """Add new Role to the database."""
    with db_session() as session:
        role = Role(name=role_name)
        session.add(role)
    return role
