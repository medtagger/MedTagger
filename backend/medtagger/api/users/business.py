"""Module responsible for business logic for users administration."""
from typing import List

from medtagger.api import InvalidArgumentsException
from medtagger.api.account.business import user_datastore, user_to_user_info
from medtagger.database import db_session
from medtagger.database.models import User
from medtagger.types import UserInfo


def get_all_users() -> List[UserInfo]:
    """Return list of all users."""
    users = User.query.all()
    user_infos = list(map(user_to_user_info, users))
    return user_infos


def set_user_role(user_id: int, role_name: str) -> None:
    """Set user's role. Old role is being replaced."""
    user = user_datastore.find_user(id=user_id)
    if user is None:
        raise InvalidArgumentsException("User not found")
    role = user_datastore.find_role(role_name)
    if role is None:
        raise InvalidArgumentsException("Role not found")
    with db_session() as session:
        user.roles.clear()
        user.roles.append(role)
        session.add(user)
