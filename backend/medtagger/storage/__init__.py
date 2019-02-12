"""Definition of storage for MedTagger."""
from typing import Dict

from medtagger.config import AppConfiguration
from medtagger.storage import filesystem, cassandra
from medtagger.storage.backend import StorageBackend


class Storage:

    storage_backend: StorageBackend = None
    available_backends: Dict[str, type] = {
        'filesystem': filesystem.FileSystemStorageBackend,
        'cassandra': cassandra.CassandraStorageBackend,
    }
    
    def __init__(self, *args, **kwargs) -> None:
        if self.storage_backend:
            return  # Do not initialize storage backend twice...

        # Fetch configuration and prepare backend
        configuration = AppConfiguration()
        backend = configuration.get('storage', 'backend', 'filesystem')
        if backend not in self.available_backends:
            raise ValueError('Invalid backend set in the MedTagger configuration file!')
        self.storage_backend = self.available_backends[backend](*args, **kwargs)

    def is_alive(self) -> bool:
        return self.storage_backend.is_alive()

    def get(self, model: type, **filters):
        return self.storage_backend.get(model, **filters)

    def create(self, model: type, **filters):
        return self.storage_backend.create(model, **filters)

    def delete(self, model: type, **filters) -> None:
        return self.storage_backend.delete(model, **filters)
