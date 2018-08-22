"""Module responsible for business logic in all Auth endpoint."""
from medtagger.api import InvalidArgumentsException
from medtagger.api.security import hash_password, verify_user_password, generate_auth_token
from medtagger.database.models import User
from medtagger.repositories import roles as RolesRepository, users as UsersRepository


def create_user(email: str, password: str, first_name: str, last_name: str) -> int:
    """Create user with the given user information. Password is being hashed.

    :param email: user email in string format
    :param password: user password in string format
    :param first_name: user first name in string format
    :param last_name: user last name in string format

    :return: id of the new user
    """
    user = UsersRepository.get_user_by_email(email)
    if user:
        raise InvalidArgumentsException('User with this email already exists')
    password_hash = hash_password(password)
    new_user = User(email, password_hash, first_name, last_name)
    role = RolesRepository.get_role_with_name('volunteer')
    if not role:
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
    if not user:
        raise InvalidArgumentsException('User does not exist.')
    if not verify_user_password(user, password):
        raise InvalidArgumentsException('Password does not match.')
    return generate_auth_token(user)
