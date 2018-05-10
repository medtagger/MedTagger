"""Module responsible for business logic for users administration."""
from typing import List

from sqlalchemy.orm.exc import NoResultFound

from medtagger.api import InvalidArgumentsException
from medtagger.database.models import User, UserSettings
from medtagger.repositories.users import UsersRepository
from medtagger.repositories.roles import RolesRepository


def get_all_users() -> List[User]:
    """Return list of all users."""
    return UsersRepository.get_all_users()


def set_user_role(user_id: int, role_name: str) -> None:
    """Set user's role. Old role is being replaced."""
    RolesRepository.set_user_role(user_id, role_name)


def set_user_info(user_id: int, firstName: str, lastName: str) -> None:
    """Set user's information."""
    try:
        user = UsersRepository.get_user_by_id(user_id)
        UsersRepository.set_user_info(user, firstName, lastName)
    except NoResultFound:
        raise InvalidArgumentsException('User with this id does not exist.')


def set_user_settings_if_not_none(name: str, value: object) -> None:
    """Set user's settings parameter of specified name to provided value if value is not None."""
    try:
        if value is not None:
            UsersRepository.set_user_settings(name, object)
    except NoResultFound:
        raise InvalidArgumentsException('User with this id does not exist.')
