"""Module responsible for business logic for users administration."""
from typing import List

from flask_login import current_user

from medtagger.types import UserInfo
from medtagger.repositories.users import UsersRepository
from medtagger.repositories.roles import RolesRepository


def get_all_users() -> List[UserInfo]:
    """Return list of all users."""
    return UsersRepository.get_all_users()


def get_current_user_info() -> UserInfo:
    """Get current user personal information."""
    user = current_user
    return UsersRepository.user_to_user_info(user)


def set_user_role(user_id: int, role_name: str) -> None:
    """Set user's role. Old role is being replaced."""
    RolesRepository.set_user_role(user_id, role_name)
