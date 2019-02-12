from typing import Dict

from cassandra.cluster import Cluster, Session, NoHostAvailable  # pylint: disable=no-name-in-module
from cassandra.policies import RoundRobinPolicy
from cassandra.cqlengine import connection
from cassandra.io.asyncorereactor import AsyncoreConnection
from cassandra.io.geventreactor import GeventConnection

from medtagger.config import AppConfiguration
from medtagger.storage import models as unified_models
from medtagger.storage.cassandra import models as cassandra_models
from medtagger.storage.backend import StorageBackend


class CassandraStorageBackend(StorageBackend):

    MEDTAGGER_KEYSPACE = 'medtagger'

    model_mapping: Dict[type, type] = {
        unified_models.OriginalSlice: cassandra_models.CassandraOriginalSlice,
        unified_models.ProcessedSlice: cassandra_models.CassandraProcessedSlice,
        unified_models.BrushLabelElement: cassandra_models.CassandraBrushLabelElement,
    }

    def __init__(self, *args, **kwargs) -> None:
        super(CassandraStorageBackend, self).__init__()
        configuration = AppConfiguration()
        self.addresses = configuration.get('cassandra', 'addresses', 'localhost').split(',')
        self.port = configuration.getint('cassandra', 'port', 9042)
        self.default_timeout = configuration.getint('cassandra', 'default_timeout', 20)
        self.connect_timeout = configuration.getint('cassandra', 'connect_timeout', 20)

        # Create connection each time new backend is created
        self._create_connection(use_gevent=kwargs.get('use_gevent', False))

    def is_alive(self) -> bool:
        """Return boolean information if Cassandra is alive or not."""
        try:
            self.create_session()
            return True
        except NoHostAvailable:
            return False

    def get(self, model: type, **filters):
        cassandra_model = self._get_cassandra_model(model)
        return cassandra_model.get(**filters).as_unified_model()

    def create(self, model: type, **data):
        cassandra_model = self._get_cassandra_model(model)
        cassandra_model.create(**data)

    def delete(self, model: type, **filters) -> None:
        cassandra_model = self._get_cassandra_model(model)
        cassandra_model.filter(**filters).delete()

    def _get_cassandra_model(self, model: type):
        cassandra_model = self.model_mapping.get(model)
        if not cassandra_model:
            raise Exception('This model is unsupported in Cassandra Storage Backend!')
        return cassandra_model

    def create_session(self, use_gevent: bool = False) -> Session:
        """Create a Session object for above Cluster."""
        connection_class = GeventConnection if use_gevent else AsyncoreConnection
        cluster = Cluster(self.addresses, port=self.port, load_balancing_policy=RoundRobinPolicy(),
                          connection_class=connection_class, connect_timeout=self.connect_timeout)
        session = cluster.connect()
        session.default_timeout = self.default_timeout
        return session

    def _create_connection(self, use_gevent: bool = False) -> None:
        """Create a Session object for above Cluster."""
        connection_class = GeventConnection if use_gevent else AsyncoreConnection
        connection.setup(self.addresses, self.MEDTAGGER_KEYSPACE, port=self.port, load_balancing_policy=RoundRobinPolicy(),
                         connection_class=connection_class, connect_timeout=self.connect_timeout)
        session = connection.get_session()
        session.default_timeout = self.default_timeout
