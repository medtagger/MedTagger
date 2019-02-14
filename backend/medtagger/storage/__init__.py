"""Definition of storage for MedTagger."""
from typing import Any, Dict, Type, Optional

from medtagger import config
from medtagger.storage import filesystem, cassandra, backend as storage_backend, models


class Storage:
    """Unified storage mechanism."""

    backend: Optional[storage_backend.StorageBackend] = None
    available_backends: Dict[str, Type[storage_backend.StorageBackend]] = {
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
        assert self.backend, 'Invalid backend!'
        return self.backend.is_alive()

    def get(self, model: Type[models.StorageModelTypeVar], **filters: Any) -> models.StorageModelTypeVar:
        """Fetch entry for a given model using passed filters."""
        assert self.backend, 'Invalid backend!'
        return self.backend.get(model, **filters)

    def create(self, model: Type[models.StorageModel], **data: Any) -> models.StorageModel:
        """Create new entry for a given model and passed data."""
        assert self.backend, 'Invalid backend!'
        return self.backend.create(model, **data)

    def delete(self, model: Type[models.StorageModel], **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        assert self.backend, 'Invalid backend!'
        self.backend.delete(model, **filters)
