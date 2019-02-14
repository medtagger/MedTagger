"""Unified models that can be found in the Storage."""
import abc
from typing import TypeVar


StorageModelTypeVar = TypeVar('StorageModelTypeVar', bound='StorageModel')


class InternalStorageModel:
    """Internal representation of a Storage Model."""  # pylint: disable=too-few-public-methods

    def as_unified_model(self) -> 'StorageModel':
        """Convert internal model representation into unified model."""
        raise NotImplementedError('This model does not implement conversion to Unified Model!')


class StorageModel(abc.ABC):
    """Model definition that can be used by Storage."""  # pylint: disable=too-few-public-methods

    pass  # pylint: disable=unnecessary-pass


class OriginalSlice(StorageModel):
    """Model for Original DICOM Slices."""  # pylint: disable=too-few-public-methods

    def __init__(self, _id: str, image: bytes) -> None:
        """Initialize model.

        :param id: GUID that is the same as for Slice object in the SQL DB
        :param image: bytes representing Original DICOM image
        """
        self.id = _id
        self.image = image


class ProcessedSlice(StorageModel):
    """Model for Processed DICOM Slices."""  # pylint: disable=too-few-public-methods

    def __init__(self, _id: str, image: bytes) -> None:
        """Initialize model.

        :param id: GUID that is the same as for Slice object in the SQL DB
        :param image: bytes representing Processed DICOM image
        """
        self.id = _id
        self.image = image


class BrushLabelElement(StorageModel):
    """Model for Brush Label Element's image."""  # pylint: disable=too-few-public-methods

    def __init__(self, _id: str, image: bytes) -> None:
        """Initialize model.

        :param id: GUID that is the same as for Slice object in the SQL DB
        :param image: bytes representing Brush label as an image
        """
        self.id = _id
        self.image = image
