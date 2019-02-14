"""Definition of storage for MedTagger."""
from typing import Dict, Any

from medtagger import config
from medtagger.storage import filesystem, cassandra, backend as storage_backend, models


class Storage:
    """Unified storage mechanism."""

    backend: storage_backend.StorageBackend = None
    available_backends: Dict[str, type] = {
        'filesystem': filesystem.FileSystemStorageBackend,
        'cassandra': cassandra.CassandraStorageBackend,
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize Storage against backend defined in the configuration."""
        if self.backend:
            return  # Do not initialize storage backend twice...

        # Fetch configuration and prepare storage backend
        configuration = config.AppConfiguration()
        backend = configuration.get('storage', 'backend', 'filesystem')
        if backend not in self.available_backends:
            raise ValueError('Invalid backend set in the MedTagger configuration file!')
        self.backend = self.available_backends[backend](*args, **kwargs)

    def is_alive(self) -> bool:
        """Check if Storage backend is still alive or not."""
        return self.backend.is_alive()

    def get(self, model: models.StorageModel, **filters: Any) -> models.StorageModel:
        """Fetch entry for a given model using passed filters."""
        internal_model = self.backend.get(model, **filters)
        return internal_model.as_unified_model()

    def create(self, model: models.StorageModel, **data: Any) -> models.StorageModel:
        """Create new entry for a given model and passed data."""
        internal_model = self.backend.create(model, **data)
        return internal_model.as_unified_model()

    def delete(self, model: models.StorageModel, **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        self.backend.delete(model, **filters)
