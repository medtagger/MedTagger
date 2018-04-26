"""Storage for all utility functions."""
from starbase import Connection
from retrying import retry
from requests.exceptions import ConnectionError as RequestsConnectionError

from medtagger.config import AppConfiguration


@retry(stop_max_attempt_number=5, wait_random_min=200, wait_random_max=1000,
       retry_on_exception=lambda ex: isinstance(ex, RequestsConnectionError))
def get_connection_to_hbase() -> Connection:
    """Fetch configuration data and create HBase connection.

    :return: connection to HBase using Starbase library
    """
    configuration = AppConfiguration()
    host = configuration.get('hbase', 'host', fallback='localhost')
    port = configuration.getint('hbase', 'rest_port', fallback=8080)
    connection = Connection(host=host, port=port)
    connection.tables()  # Test if the connection was properly set up
    return connection


def user_agrees(prompt_message: str) -> bool:
    """Ask user a question and ask him/her for True/False answer (default answer is False).

    :param prompt_message: message that will be prompted to user
    :return: boolean information if user agrees or not
    """
    answer = input(prompt_message + ' [y/N] ')
    return answer.lower() in ['y', 'yes', 't', 'true']
