"""Storage Backend definition that can be used in Storage mechanism."""
import abc
from typing import Any

from medtagger.storage.models import StorageModel


class StorageBackend(abc.ABC):
    """Interface for Storage Backend supported by Storage."""

    def is_alive(self) -> bool:
        """Check if Storage backend is still alive or not."""
        raise NotImplementedError('This method is not implemented!')

    def get(self, model: StorageModel, **filters: Any) -> StorageModel:
        """Fetch entry for a given model using passed filters."""
        raise NotImplementedError('This method is not implemented!')

    def create(self, model: StorageModel, **data: Any) -> StorageModel:
        """Create new entry for a given model and passed data."""
        raise NotImplementedError('This method is not implemented!')

    def delete(self, model: StorageModel, **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        raise NotImplementedError('This method is not implemented!')
