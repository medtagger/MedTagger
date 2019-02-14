"""Module for description of a File System backend for Storage."""
from typing import Any, Dict, Type, cast

import os

from medtagger import config
from medtagger.storage import backend, models as unified_models
from medtagger.storage.filesystem import models as filesystem_models


class FileSystemStorageBackend(backend.StorageBackend):
    """Storage backend based on a simple File System."""

    model_mapping: Dict[Type[unified_models.StorageModel], Type[filesystem_models.FileSystemModel]] = {
        unified_models.OriginalSlice: filesystem_models.FileSystemOriginalSlice,
        unified_models.ProcessedSlice: filesystem_models.FileSystemProcessedSlice,
        unified_models.BrushLabelElement: filesystem_models.FileSystemBrushLabelElement,
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize Storage backend based on passed arguments."""
        # pylint: disable=unused-argument
        super(FileSystemStorageBackend, self).__init__()
        configuration = config.AppConfiguration()
        self.directory = configuration.get('filesystem', 'directory', '/tmp/medtagger')
        os.makedirs(self.directory, exist_ok=True)

    def is_alive(self) -> bool:
        """Check if Storage backend is still alive or not."""
        return os.access(self.directory, os.R_OK) and os.access(self.directory, os.W_OK)

    def get(self, model: Type[unified_models.StorageModelTypeVar], **filters: Any) \
            -> unified_models.StorageModelTypeVar:
        """Fetch entry for a given model using passed filters."""
        filesystem_model = self._get_filesystem_model(model)
        internal_model = filesystem_model.get(self.directory, **filters)
        return cast(unified_models.StorageModelTypeVar, internal_model.as_unified_model())

    def create(self, model: Type[unified_models.StorageModelTypeVar], **data: Any) \
            -> unified_models.StorageModelTypeVar:
        """Create new entry for a given model and passed data."""
        filesystem_model = self._get_filesystem_model(model)
        internal_model = filesystem_model.create(self.directory, **data)
        return cast(unified_models.StorageModelTypeVar, internal_model.as_unified_model())

    def delete(self, model: Type[unified_models.StorageModel], **filters: Any) -> None:
        """Delete an entry for a given model using passed filters."""
        filesystem_model = self._get_filesystem_model(model)
        filesystem_model.delete(self.directory, **filters)

    def _get_filesystem_model(self, model: Type[unified_models.StorageModelTypeVar]) \
            -> Type[filesystem_models.FileSystemModel]:
        filesystem_model = self.model_mapping.get(model)
        if not filesystem_model:
            raise Exception('This model is unsupported in FileSystem Storage Backend!')
        return filesystem_model
