"""Module responsible for business logic for user's account management."""
from flask_login import current_user
from flask_security import SQLAlchemyUserDatastore, Security, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from medtagger.api import InvalidArgumentsException
from medtagger.database import db_session, db
from medtagger.database.models import User, Role
from medtagger.types import UserInfo

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()


def create_user(email: str, password: str, first_name: str, last_name: str) -> int:
    """Create user with the given user information. Password is being hashed.

    :return: id of the new user
    """
    user_with_email = User.query.filter_by(email=email).first()
    if user_with_email is not None:
        raise InvalidArgumentsException("User with given email does already exist.")
    password_hash = generate_password_hash(password)
    new_user = User(email, password_hash, first_name, last_name)
    role = user_datastore.find_role('volunteer')
    new_user.roles.append(role)
    with db_session() as session:
        session.add(new_user)
    return new_user.id


def sign_in_user(email: str, password: str) -> str:
    """Sign in user using given username and password.

    :return: authentication token
    """
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise InvalidArgumentsException("User does not exist.")
    password_match = check_password_hash(user.password, password)
    if not password_match:
        raise InvalidArgumentsException("Password does not match.")
    login_user(user)
    return user.get_auth_token()


def sign_out_user() -> None:
    """Sign out the current user."""
    logout_user()


def get_current_user_info() -> UserInfo:
    """Get current user personal information."""
    user = current_user
    return user_to_user_info(user)


def user_to_user_info(user: User) -> UserInfo:
    """Map user entity to UserInfo tuple."""
    role = user.roles[0].name
    return UserInfo(id=user.id,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    role=role)
