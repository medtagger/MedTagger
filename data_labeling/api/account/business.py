"""Module responsible for business logic for user management"""
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from data_labeling.api import InvalidArgumentsException
from data_labeling.database import db_session
from data_labeling.database.models import User
from data_labeling.types import UserInfo

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id: str) -> User:
    """Load user handler - required by flask-login"""
    return User.query.get(user_id)


def create_user(email: str, password: str, first_name: str, last_name: str) -> int:
    """Create user with the given user information. Password is being hashed.
    :return: id of the new user
    """
    user_with_email = User.query.filter_by(email=email).first()
    if user_with_email is not None:
        raise InvalidArgumentsException("User with given email does already exist.")
    password_hash = generate_password_hash(password)
    new_user = User(email, password_hash, first_name, last_name)
    with db_session() as session:
        session.add(new_user)
    return new_user.id


def sign_in_user(email: str, password: str) -> None:
    """Sign in user using given username and password."""
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise InvalidArgumentsException("User does not exist.")
    password_match = check_password_hash(user.password, password)
    if not password_match:
        raise InvalidArgumentsException("Password does not match.")
    login_user(user)


def sign_out_user() -> None:
    """Sign out the current user"""
    logout_user()


def get_current_user_info() -> UserInfo:
    """Get current user personal information."""
    user = current_user
    return UserInfo(email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name)
