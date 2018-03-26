"""Methods related to API authorization control."""
from typing import Callable, Optional, Any, cast
from functools import wraps

from flask import g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from passlib.apps import custom_app_context as pwd_context

from medtagger.config import AppConfiguration
from medtagger.database.models import User
from medtagger.api.exceptions import UnauthorizedException

TOKEN_EXPIRE_TIME = 24 * 60 * 60  # 24 hours


def auth_error_handler() -> None:
    """Handle authorization error.

    Raises an exception that will be handled by Flask-RESTPlus error handling.
    """
    raise UnauthorizedException('Invalid credentials.')


auth = HTTPTokenAuth()
login_required = auth.login_required
auth.auth_error_callback = auth_error_handler


def role_required(*required_roles: str) -> Callable:
    """Make one of passed Roles required for given method."""
    def wrapper(wrapped_method: Callable) -> Callable:
        """Wrap passed method to check User's roles."""
        @wraps(wrapped_method)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            """Check User's roles and raise an exception in case of unauthorized use."""
            if not g.user:
                raise UnauthorizedException('You are not logged in.')
            if g.user.role.name not in required_roles:  # One of required roles is sufficient
                raise UnauthorizedException('You don\'t have required roles to access this method.')
            return wrapped_method(*args, **kwargs)
        return decorated
    return wrapper


def hash_password(password: str) -> str:
    """Hash given password."""
    return pwd_context.encrypt(password)


def verify_user_password(user: User, password: str) -> bool:
    """Verify User's password with the one that was given on login page."""
    return pwd_context.verify(password, user.password)


def generate_auth_token(user: User, expiration: int = TOKEN_EXPIRE_TIME) -> str:
    """Generate token that will be then used for User's authorization.

    :param user: User's database object
    :param expiration: expiration time (in minutes) after such token should expire
    :return: authorization token as a string
    """
    serializer = Serializer(AppConfiguration.get('api', 'secret_key'), expires_in=expiration)
    token_bytes = cast(bytes, serializer.dumps({'id': user.id}))
    return token_bytes.decode('ascii')


def get_user_by_token(token: str) -> Optional[User]:
    """Return User using passed token.

    :param token: authorization token
    :return: User if found or None
    """
    serializer = Serializer(AppConfiguration.get('api', 'secret_key'))
    try:
        data = serializer.loads(token)
    except SignatureExpired:
        return None  # Valid token, but expired
    except BadSignature:
        return None  # Invalid token
    return User.query.get(data['id'])


@auth.verify_token
def verify_token(token: str) -> bool:
    """Verify passed token for its correctness.

    It also saves User's database object to the Flask `g` object for further use.

    :param token: authorization token
    :return: boolean information about token correctness
    """
    user = get_user_by_token(token)
    if not user:
        return False
    g.user = user
    return True
