"""Module responsible for business logic in all Auth endpoint."""
from flask_security import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from medtagger.api import InvalidArgumentsException
from medtagger.database.models import User
from medtagger.repositories.roles import RolesRepository
from medtagger.repositories.users import UsersRepository


def create_user(email: str, password: str, first_name: str, last_name: str) -> int:
    """Create user with the given user information. Password is being hashed.

    :param email: user email in string format
    :param password: user password in string format
    :param first_name: user first name in string format
    :param last_name: user last name in string format

    :return: id of the new user
    """
    user = UsersRepository.get_user_by_email(email)
    if user is not None:
        raise InvalidArgumentsException('User with this email already exist')
    password_hash = generate_password_hash(password)
    new_user = User(email, password_hash, first_name, last_name)
    role = RolesRepository.get_role_with_name('volunteer')
    if role is None:
        raise InvalidArgumentsException('Role does not exist.')
    new_user.roles.append(role)
    return UsersRepository.add_new_user(new_user)


def sign_in_user(email: str, password: str) -> str:
    """Sign in user using given username and password.

    :param email: user email in string format
    :param password: user password in string format

    :return: authentication token
    """
    user = UsersRepository.get_user_by_email(email)
    if user is None:
        raise InvalidArgumentsException('User does not exist.')
    password_match = check_password_hash(user.password, password)
    if not password_match:
        raise InvalidArgumentsException('Password does not match.')
    login_user(user)
    return user.get_auth_token()


def sign_out_user() -> None:
    """Sign out the current user."""
    logout_user()
