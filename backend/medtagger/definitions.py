"""Module responsible for storage of all definitions that may appear across whole project."""
from enum import Enum


class DicomTags(Enum):
    """All tags supported by MedTagger that can be read from DICOM."""

    SLICE_LOCATION = '0020|1041'
    IMAGE_POSITION_PATIENT = '0020|0032'
    RESCALE_INTERCEPT = '0028|1052'
    RESCALE_SLOPE = '0028|1053'
    RESCALE_TYPE = '0028|1054'
    PIXEL_SPACING = '0028|0030'