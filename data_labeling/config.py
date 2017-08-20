"""Module responsible for reading data from configuration files"""
import os

from configparser import ConfigParser


DEFAULT_CONFIGURATION_NAME = os.environ.get('CONFIG_FILE', 'backend_api.conf')


class ConfigurationFile(ConfigParser):  # pylint: disable=too-many-ancestors; Base class inherits too many times...
    """Class that represents configuration file"""

    def __init__(self, file_name: str = DEFAULT_CONFIGURATION_NAME) -> None:
        """Initializer for configuration file

        :param file_name: name of a configuration file
        """
        super(ConfigurationFile, self).__init__()
        self.read(file_name)
