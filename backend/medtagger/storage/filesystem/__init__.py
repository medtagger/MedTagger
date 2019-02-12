from typing import Dict

import os

from medtagger.config import AppConfiguration
from medtagger.storage import models as unified_models
from medtagger.storage.filesystem import models as filesystem_models
from medtagger.storage.backend import StorageBackend


class FileSystemStorageBackend(StorageBackend):

    model_mapping: Dict[type, type] = {
        unified_models.OriginalSlice: filesystem_models.FileSystemOriginalSlice,
        unified_models.ProcessedSlice: filesystem_models.FileSystemProcessedSlice,
        unified_models.BrushLabelElement: filesystem_models.FileSystemBrushLabelElement,
    }

    def __init__(self, *args, **kwargs) -> None:
        super(FileSystemStorageBackend, self).__init__()
        configuration = AppConfiguration()
        self.directory = configuration.get('filesystem', 'directory', '/tmp/medtagger')
        os.makedirs(self.directory, exist_ok=True)

    def is_alive(self) -> bool:
        return os.access(self.directory, os.R_OK) and os.access(self.directory, os.W_OK)

    def get(self, model: type, **filters):
        filesystem_model = self._get_filesystem_model(model)
        return filesystem_model.get(self.directory, **filters)

    def create(self, model: type, **data):
        filesystem_model = self._get_filesystem_model(model)
        return filesystem_model.create(self.directory, **data)

    def delete(self, model: type, **filters) -> None:
        filesystem_model = self._get_filesystem_model(model)
        return filesystem_model.delete(self.directory, **filters)

    def _get_filesystem_model(self, model: type):
        filesystem_model = self.model_mapping.get(model)
        if not filesystem_model:
            raise Exception('This model is unsupported in FileSystem Storage Backend!')
        return filesystem_model
