"""Exceptions used across whole API."""


class BaseHTTPException(Exception):
    """Base class for all HTTP Exceptions."""

    pass


class UnauthorizedException(BaseHTTPException):
    """Exception designed to use once there was an authorization error during business logic processing."""

    pass


class NotFoundException(BaseHTTPException):
    """Exception designed to use while the object that user was looking for could not be found."""

    pass


class InvalidArgumentsException(BaseHTTPException):
    """Exception designed to use with invalid arguments (400 status code)."""

    pass


class AccessForbiddenException(BaseHTTPException):
    """Exception designed to use while the user does not have a privilege to perform action."""

    pass
