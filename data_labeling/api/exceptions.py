"""Exceptions used across whole API"""


class BaseHTTPException(Exception):
    """Base class for all HTTP Exceptions"""
    pass


class BusinessLogicException(BaseHTTPException):
    """Exception designed to use once there was an error during business logic processing"""
    pass


class NotFoundException(BusinessLogicException):
    """Exception designed to use while the object that user was looking for could not be found"""
    pass


class InvalidArgumentsException(BaseHTTPException):
    """Exception designed to use with invalid arguments (400 status code)"""
    pass
