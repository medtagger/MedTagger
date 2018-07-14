"""Module responsible for storage of all definitions that may appear across whole project."""
from enum import Enum


class DicomTag(Enum):
    """Define all tags supported by MedTagger that can be read from DICOM."""

    SLICE_LOCATION = '0020|1041'
    IMAGE_POSITION_PATIENT = '0020|0032'
    RESCALE_INTERCEPT = '0028|1052'
    RESCALE_SLOPE = '0028|1053'
    RESCALE_TYPE = '0028|1054'
    PIXEL_SPACING = '0028|0030'
    ROWS = '0028|0010'
    COLUMNS = '0028|0011'
    MODALITY = '0008|0060'


class SliceOrientation(Enum):
    """Define available Slice orientations."""

    X = 'X'
    Y = 'Y'
    Z = 'Z'


class LabelStatus(Enum):
    """Define available statuses for Label."""

    VALID = 'VALID'
    INVALID = 'INVALID'
    NOT_VERIFIED = 'NOT_VERIFIED'


class ScanStatus(Enum):
    """Define available statuses for Scan."""

    NEW = 'NEW'
    STORED = 'STORED'
    PROCESSING = 'PROCESSING'
    AVAILABLE = 'AVAILABLE'


class SliceStatus(Enum):
    """Define available statuses for Slice."""

    NEW = 'NEW'
    STORED = 'STORED'
    PROCESSED = 'PROCESSED'


class LabelVerificationStatus(Enum):
    """Define available verification status for Label."""

    VERIFIED = 'VERIFIED'
    NOT_VERIFIED = 'NOT_VERIFIED'


class LabelElementStatus(Enum):
    """Define available status for Label Element."""

    VALID = 'VALID'
    INVALID = 'INVALID'
    NOT_VERIFIED = 'NOT_VERIFIED'


class LabelTool(Enum):
    """Defines available Label Tools."""

    RECTANGLE = 'RECTANGLE'
    BRUSH = 'BRUSH'
    POINT = 'POINT'
    CHAIN = 'CHAIN'
