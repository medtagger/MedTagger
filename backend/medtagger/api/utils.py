"""Utils methods used across whole API."""
from flask_login import current_user

from medtagger.database.models import User


def get_current_user() -> User:
    """Get current logged in user."""
    return current_user
