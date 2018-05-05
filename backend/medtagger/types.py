"""Module containing all custom types."""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)
SliceID = NewType('SliceID', str)
LabelID = NewType('LabelID', str)
LabelElementID = NewType('LabelElementID', str)
LabelTagID = NewType('LabelTagID', int)
RectangularLabelElementID = NewType('RectangularLabelElementID', str)

ScanMetadata = NamedTuple('ScanMetadata', [('scan_id', ScanID), ('number_of_slices', int)])

SliceLocation = NewType('SliceLocation', float)
SlicePosition = NamedTuple('SlicePosition', [('x', float), ('y', float), ('z', float)])

LabelPosition = NamedTuple('LabelPosition', [('x', float), ('y', float), ('slice_index', int)])
LabelShape = NamedTuple('LabelShape', [('width', float), ('height', float)])

LabelingTime = NewType('LabelingTime', float)
