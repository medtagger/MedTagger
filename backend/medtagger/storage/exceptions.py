"""Module for exceptions that may be thrown by Storage mechanism."""


class NotFound(Exception):
    """Exception thrown if looking entry does not exist in the Storage."""

    pass  # pylint: disable=unnecessary-pass
