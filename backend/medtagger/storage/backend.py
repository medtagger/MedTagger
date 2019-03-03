"""Storage Backend definition that can be used in Storage mechanism."""
import abc
from typing import Any, Type

from medtagger.storage import models


class StorageBackend(abc.ABC):
    """Interface for Storage Backend supported by Storage."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize backend for Storage."""
        pass  # pylint: disable=unnecessary-pass

    def is_alive(self) -> bool:
        """Check if Storage backend is still alive or not."""
        raise NotImplementedError('This method is not implemented!')

    def get(self, model: Type[models.StorageModelTypeVar], **filters: Any) -> models.StorageModelTypeVar:
        """Fetch entry for a given model using passed filters."""
        raise NotImplementedError('This method is not implemented!')

    def create(self, model: Type[models.StorageModel], **data: Any) -> models.StorageModel:
        """Create new entry for a given model and passed data."""
        raise NotImplementedError('This method is not implemented!')

    def delete(self, model: Type[models.StorageModel], **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        raise NotImplementedError('This method is not implemented!')
