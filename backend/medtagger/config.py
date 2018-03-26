"""Module responsible for reading data from application configuration."""
import os
from typing import Any


class AppConfiguration(object):
    """Class that represents application configuration."""

    def __init__(self) -> None:
        """Initialize application configuration."""
        pass

    @staticmethod
    def get(namespace: str, key: str, fallback: Any = None) -> Any:
        """Return value of a given configuration entry.

        :param namespace: name of a namespace for given entry
        :param key: key for which it should return value from given namespace
        :param fallback: default value returned if key was not found
        :return: value for given entry
        """
        variable_name = 'MEDTAGGER__' + namespace.upper() + '_' + key.upper()
        return os.environ.get(variable_name, fallback)

    @staticmethod
    def getint(namespace: str, key: str, fallback: int = 0) -> int:
        """Return integer value for given key in namespace."""
        return int(AppConfiguration.get(namespace, key, fallback))

    @staticmethod
    def getboolean(namespace: str, key: str, fallback: bool = False) -> bool:
        """Return boolean value for given key in namespace."""
        return bool(AppConfiguration.getint(namespace, key, fallback))
