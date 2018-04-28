"""Module responsible for business logic for users administration."""
from typing import List

from medtagger.database.models import User
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
    UsersRepository.set_user_info(user_id, firstName, lastName)