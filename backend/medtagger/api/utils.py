"""Utils methods used across whole API."""
from flask import g

from medtagger.database.models import User


def get_current_user() -> User:
    """Get current logged in user."""
    return g.user
