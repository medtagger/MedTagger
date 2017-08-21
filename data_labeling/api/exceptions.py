"""Exceptions used across whole API"""


class BaseHTTPException(Exception):
    """Base class for all HTTP Exceptions"""
    pass


class InvalidArgumentsException(BaseHTTPException):
    """Exception designed to use with invalid arguments (400 status code)"""
    pass
