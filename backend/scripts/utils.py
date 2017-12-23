"""Storage for all utility functions."""
from starbase import Connection
from data_labeling.config import AppConfiguration


def get_connection_to_hbase() -> Connection:
    """Fetch configuration data and create HBase connection.

    :return: connection to HBase using Starbase library
    """
    configuration = AppConfiguration()
    host = configuration.get('hbase', 'host', fallback='localhost')
    port = configuration.getint('hbase', 'rest_port', fallback=8080)
    return Connection(host=host, port=port)


def user_agrees(prompt_message: str) -> bool:
    """Ask user a question and ask him/her for True/False answer (default answer is False).

    :param prompt_message: message that will be prompted to user
    :return: boolean information if user agrees or not
    """
    answer = input(prompt_message + ' [y/N] ')
    return answer.lower() in ['y', 'yes', 't', 'true']
