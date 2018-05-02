"""Module containing all custom types."""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)
SliceID = NewType('SliceID', str)
LabelID = NewType('LabelID', str)
LabelElementID = NewType('LabelElementID', str)
<<<<<<< 54ea58afc625560e1e697c3e489f931b5b52d051
LabelTagID = NewType('LabelTagID', str)
=======
LabelTagID = NewType('LabelTagID', int)

ScanMetadata = NamedTuple('ScanMetadata', [('scan_id', ScanID), ('number_of_slices', int)])
>>>>>>> Api and tests (#206)

SliceLocation = NewType('SliceLocation', float)
SlicePosition = NamedTuple('SlicePosition', [('x', float), ('y', float), ('z', float)])

LabelPosition = NamedTuple('LabelPosition', [('x', float), ('y', float), ('slice_index', int)])
LabelShape = NamedTuple('LabelShape', [('width', float), ('height', float)])
LabelSelectionBinaryMask = NewType('LabelSelectionBinaryMask', str)

LabelingTime = NewType('LabelingTime', float)
