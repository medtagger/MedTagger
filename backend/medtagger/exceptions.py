"""All available Exceptions for whole project."""


class MedTaggerException(Exception):
    """Base class for all HTTP Exceptions."""

    pass


class UnsupportedActionException(MedTaggerException):
    """Exception for unsupported Action."""

    pass


class InvalidResponseException(MedTaggerException):
    """Exception for invalid Response."""

    pass


class InternalErrorException(MedTaggerException):
    """Exception designed to use to indicate internal errors (like DB/Storage error)."""

    pass
