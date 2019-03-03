"""Module responsible for handling File System internal representation of each model."""
import os
from typing import Any, BinaryIO

from medtagger.storage import exceptions, models


class FileSystemModel(models.InternalStorageModel):
    """Internal representation of a File System model."""

    MODEL_DIRECTORY = 'UNKNOWN'

    @classmethod
    def get(cls, filesystem_directory: str, **filters: Any) -> 'FileSystemModel':
        """Fetch instance of a model from the File System's directory.

        :param filesystem_directory: directory used by Storage to store its internal files
        :param filters: key-value arguments representing all filters that will be used to find given file
        :return: model instance of a given class
        """
        try:
            with open(cls._get_file_location(filesystem_directory, filters['id']), 'rb') as opened_file:
                return cls.from_file(opened_file)
        except FileNotFoundError:
            raise exceptions.NotFound('Not found requested entry!')

    @classmethod
    def create(cls, filesystem_directory: str, **data: Any) -> 'FileSystemModel':
        """Create an instance of a model into the File System's directory.

        :param filesystem_directory: directory used by Storage to store its internal files
        :param data: key-value arguments representing all data that will be used to create an instance of a given model
        :return: model instance of a given class
        """
        file_location = cls._get_file_location(filesystem_directory, data['id'])
        file_directory = os.path.dirname(file_location)
        os.makedirs(file_directory, exist_ok=True)
        with open(file_location, 'wb+') as opened_file:
            return cls.to_file(opened_file, **data)

    @classmethod
    def delete(cls, filesystem_directory: str, **filters: Any) -> None:
        """Delete an instance of a model from the File System's internal representation.

        :param filesystem_directory: directory used by Storage to store its internal files
        :param filters: key-value arguments representing all filters that will be used to find given file
        """
        try:
            os.remove(cls._get_file_location(filesystem_directory, filters['id']))
        except FileNotFoundError:
            raise exceptions.NotFound('Not found requested entry!')

    @classmethod
    def from_file(cls, opened_file: BinaryIO) -> 'FileSystemModel':
        """Create an instance of a File System Model based on opened binary file.

        :param opened_file: file opened in binary mode
        :return: instance of a given File System Model
        """
        raise NotImplementedError('Model cannot create its instance based on file!')

    @classmethod
    def to_file(cls, opened_file: BinaryIO, **data: Any) -> 'FileSystemModel':
        """Save a new instance of a given model into opened file with given data.

        :param opened_file: file opened in binary mode
        :param data: key-value arguments representing all data that will be used to create an instance of a given model
        :return: instance of a given File System Model
        """
        raise NotImplementedError('Model cannot save data to the file!')

    @classmethod
    def _get_file_location(cls, directory: str, _id: str) -> str:
        """Return location of a file regarding root directory used by File System's internal representation.

        :param directory: path to directory that is used as a root directory for File System
        :param _id: ID of an instance for given model
        :return: full path to the file with internal model representation
        """
        return os.path.join(directory, cls.MODEL_DIRECTORY, _id[:4], _id)


class FileSystemOriginalSlice(FileSystemModel):
    """File System's model for Original Slice."""

    MODEL_DIRECTORY = 'original_slice'

    def __init__(self, _id: str, image: bytes) -> None:
        """Initialize internal model for Original Slice."""
        self.id = _id
        self.image = image

    @classmethod
    def from_file(cls, opened_file: BinaryIO) -> 'FileSystemOriginalSlice':
        """Create an instance of a Original Slice as an internal representation based on opened binary file.

        :param opened_file: file opened in binary mode
        :return: instance of a given File System Original Slice model
        """
        _id = os.path.basename(opened_file.name)
        image = opened_file.read()
        return cls(_id, image)

    @classmethod
    def to_file(cls, opened_file: BinaryIO, **data: Any) -> 'FileSystemOriginalSlice':
        """Save a new instance of a File System Original Slice model into opened file with given data.

        :param opened_file: file opened in binary mode
        :param data: key-value arguments representing all data
        :return: instance of a given File System Original Slice model
        """
        opened_file.write(data['image'])
        return cls(_id=data['id'], image=data['image'])

    def as_unified_model(self) -> models.OriginalSlice:
        """Convert internal model representation into unified model."""
        return models.OriginalSlice(_id=self.id, image=self.image)


class FileSystemProcessedSlice(FileSystemModel):
    """File System's model for Processed Slice."""

    MODEL_DIRECTORY = 'processed_slice'

    def __init__(self, _id: str, image: bytes) -> None:
        """Initialize internal model for Processed Slice."""
        self.id = _id
        self.image = image

    @classmethod
    def from_file(cls, opened_file: BinaryIO) -> 'FileSystemProcessedSlice':
        """Create an instance of a Processed Slice as an internal representation based on opened binary file.

        :param opened_file: file opened in binary mode
        :return: instance of a given File System Processed Slice model
        """
        _id = os.path.basename(opened_file.name)
        image = opened_file.read()
        return cls(_id, image)

    @classmethod
    def to_file(cls, opened_file: BinaryIO, **data: Any) -> 'FileSystemProcessedSlice':
        """Save a new instance of a File System Processed Slice model into opened file with given data.

        :param opened_file: file opened in binary mode
        :param data: key-value arguments representing all data
        :return: instance of a given File System Processed Slice model
        """
        opened_file.write(data['image'])
        return cls(_id=data['id'], image=data['image'])

    def as_unified_model(self) -> models.ProcessedSlice:
        """Convert internal model representation into unified model."""
        return models.ProcessedSlice(_id=self.id, image=self.image)


class FileSystemBrushLabelElement(FileSystemModel):
    """File System's model for Brush Label Element."""

    MODEL_DIRECTORY = 'brush_label_element'

    def __init__(self, _id: str, image: bytes) -> None:
        """Initialize internal model for Brush Label Element."""
        self.id = _id
        self.image = image

    @classmethod
    def from_file(cls, opened_file: BinaryIO) -> 'FileSystemBrushLabelElement':
        """Create an instance of a Brush Label Element as an internal representation based on opened binary file.

        :param opened_file: file opened in binary mode
        :return: instance of a given File System Brush Label Element model
        """
        _id = os.path.basename(opened_file.name)
        image = opened_file.read()
        return cls(_id, image)

    @classmethod
    def to_file(cls, opened_file: BinaryIO, **data: Any) -> 'FileSystemBrushLabelElement':
        """Save a new instance of a File System Brush Label Element model into opened file with given data.

        :param opened_file: file opened in binary mode
        :param data: key-value arguments representing all data
        :return: instance of a given File System Brush Label Element model
        """
        opened_file.write(data['image'])
        return cls(_id=data['id'], image=data['image'])

    def as_unified_model(self) -> models.BrushLabelElement:
        """Convert internal model representation into unified model."""
        return models.BrushLabelElement(_id=self.id, image=self.image)
