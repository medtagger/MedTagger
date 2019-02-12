"""Definition of storage for MedTagger."""
from typing import Dict

from medtagger.config import AppConfiguration
from medtagger.storage import filesystem, cassandra
from medtagger.storage.backend import StorageBackend


class Storage:
    """Unified storage mechanism."""

    backend: StorageBackend = None
    available_backends: Dict[str, type] = {
        'filesystem': filesystem.FileSystemStorageBackend,
        'cassandra': cassandra.CassandraStorageBackend,
    }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize Storage against backend defined in the configuration."""
        if self.backend:
            return  # Do not initialize storage backend twice...

        # Fetch configuration and prepare storage backend
        configuration = AppConfiguration()
        backend = configuration.get('storage', 'backend', 'filesystem')
        if backend not in self.available_backends:
            raise ValueError('Invalid backend set in the MedTagger configuration file!')
        self.backend = self.available_backends[backend](*args, **kwargs)

    def is_alive(self) -> bool:
        """Check if Storage backend is still alive or not."""
        return self.backend.is_alive()

    def get(self, model: StorageModel, **filters: Any) -> StorageModel:
        """Fetch entry for a given model using passed filters."""
        return self.backend.get(model, **filters)

    def create(self, model: StorageModel, **data: Any) -> StorageModel:
        """Create new entry for a given model and passed data."""
        return self.backend.create(model, **data)

    def delete(self, model: StorageModel, **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        self.backend.delete(model, **filters)
