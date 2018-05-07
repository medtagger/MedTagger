"""Definition of storage for MedTagger."""
from cassandra.cluster import Cluster, Session, NoHostAvailable  # pylint: disable=no-name-in-module
from cassandra.policies import RoundRobinPolicy
from cassandra.cqlengine import connection
from cassandra.io.asyncorereactor import AsyncoreConnection
from cassandra.io.geventreactor import GeventConnection

from medtagger.config import AppConfiguration


MEDTAGGER_KEYSPACE = 'medtagger'

configuration = AppConfiguration()
addresses = configuration.get('cassandra', 'addresses', 'localhost').split(',')
port = configuration.getint('cassandra', 'port', 9042)
default_timeout = configuration.getint('cassandra', 'default_timeout', 20)


def create_session(use_gevent: bool = False) -> Session:
    """Create a Session object for above Cluster."""
    connection_class = GeventConnection if use_gevent else AsyncoreConnection
    cluster = Cluster(addresses, port=port, load_balancing_policy=RoundRobinPolicy(), connection_class=connection_class)
    session = cluster.connect()
    session.default_timeout = default_timeout
    return session


def create_connection(use_gevent: bool = False) -> None:
    """Create a Session object for above Cluster."""
    connection_class = GeventConnection if use_gevent else AsyncoreConnection
    connection.setup(addresses, MEDTAGGER_KEYSPACE, port=port, load_balancing_policy=RoundRobinPolicy(),
                     connection_class=connection_class)
    session = connection.get_session()
    session.default_timeout = default_timeout


def is_alive() -> bool:
    """Return boolean information if Cassandra is alive or not."""
    try:
        create_session()
        return True
    except NoHostAvailable:
        return False
