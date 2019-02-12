"""Unified models that can be found in the Storage."""
import abc


class StorageModel(abc.ABC):
    """Model definition that can be used by Storage."""

    pass


class OriginalSlice(StorageModel):
    """Model for Original DICOM Slices."""

    def __init__(self, id: str, image: bytes) -> None:
        """Initialize model.

        :param id: GUID that is the same as for Slice object in the SQL DB
        :param image: bytes representing Original DICOM image
        """
        self.id = id
        self.image = image


class ProcessedSlice(StorageModel):
    """Model for Processed DICOM Slices."""

    def __init__(self, id: str, image: bytes) -> None:
        """Initialize model.

        :param id: GUID that is the same as for Slice object in the SQL DB
        :param image: bytes representing Processed DICOM image
        """
        self.id = id
        self.image = image


class BrushLabelElement(StorageModel):
    """Model for Brush Label Element's image."""

    def __init__(self, id: str, image: bytes) -> None:
        """Initialize model.

        :param id: GUID that is the same as for Slice object in the SQL DB
        :param image: bytes representing Brush label as an image
        """
        self.id = id
        self.image = image
