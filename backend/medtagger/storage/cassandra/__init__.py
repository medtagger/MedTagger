"""Module for description of a Cassandra backend for Storage."""
from typing import Any, Dict

from cassandra.cluster import Cluster, Session, NoHostAvailable  # pylint: disable=no-name-in-module
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import DoesNotExist
from cassandra.io.asyncorereactor import AsyncoreConnection
from cassandra.io.geventreactor import GeventConnection
from cassandra.policies import RoundRobinPolicy

from medtagger import config
from medtagger.storage import backend, models as unified_models, exceptions
from medtagger.storage.cassandra import models as cassandra_models


class CassandraStorageBackend(backend.StorageBackend):
    """Storage backend based on Cassandra."""

    MEDTAGGER_KEYSPACE = 'medtagger'

    model_mapping: Dict[unified_models.StorageModel, unified_models.InternalStorageModel] = {
        unified_models.OriginalSlice: cassandra_models.CassandraOriginalSlice,
        unified_models.ProcessedSlice: cassandra_models.CassandraProcessedSlice,
        unified_models.BrushLabelElement: cassandra_models.CassandraBrushLabelElement,
    }

    def __init__(self, *args: Any, use_gevent: bool = False, **kwargs: Any) -> None:
        """Initialize Storage backend based on passed arguments.

        :param use_gevent: boolean flag that indicates if backend is run behind Gevent or not
        """
        # pylint: disable=unused-argument
        super(CassandraStorageBackend, self).__init__()
        configuration = config.AppConfiguration()
        self.addresses = configuration.get('cassandra', 'addresses', 'localhost').split(',')
        self.port = configuration.getint('cassandra', 'port', 9042)
        self.default_timeout = configuration.getint('cassandra', 'default_timeout', 20)
        self.connect_timeout = configuration.getint('cassandra', 'connect_timeout', 20)

        # Create connection each time new backend is created
        self._create_connection(use_gevent=use_gevent)

    def is_alive(self) -> bool:
        """Return boolean information if Cassandra is alive or not."""
        try:
            self.create_session()
            return True
        except NoHostAvailable:
            return False

    def get(self, model: unified_models.StorageModel, **filters: Any) -> unified_models.StorageModel:
        """Fetch entry for a given model using passed filters."""
        try:
            cassandra_model = self._get_cassandra_model(model)
            return cassandra_model.get(**filters).as_unified_model()
        except DoesNotExist:
            raise exceptions.NotFound('Did not found requested entry!')

    def create(self, model: unified_models.StorageModel, **data: Any) -> unified_models.StorageModel:
        """Create new entry for a given model and passed data."""
        cassandra_model = self._get_cassandra_model(model)
        cassandra_model.create(**data)

    def delete(self, model: unified_models.StorageModel, **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        try:
            cassandra_model = self._get_cassandra_model(model)
            cassandra_model.filter(**filters).delete()
        except DoesNotExist:
            raise exceptions.NotFound('Did not found requested entry!')

    def _get_cassandra_model(self, model: unified_models.StorageModel) -> unified_models.InternalStorageModel:
        """Convert unified Storage model into internal Storage model."""
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
        connection.setup(self.addresses, self.MEDTAGGER_KEYSPACE, port=self.port,
                         load_balancing_policy=RoundRobinPolicy(),
                         connection_class=connection_class, connect_timeout=self.connect_timeout)
        session = connection.get_session()
        session.default_timeout = self.default_timeout
