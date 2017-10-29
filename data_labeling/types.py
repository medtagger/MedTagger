"""Module containing all custom types"""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)
SliceID = NewType('SliceID', str)
LabelID = NewType('LabelID', str)
LabelSelectionID = NewType('LabelSelectionID', str)

SliceLocation = NewType('SliceLocation', float)
SlicePosition = NamedTuple('SlicePosition', [('x', float), ('y', float), ('z', float)])

PickledDicomImage = NewType('PickledDicomImage', str)

LabelPosition = NamedTuple('LabelPosition', [('x', float), ('y', float), ('slice_index', int)])
LabelShape = NamedTuple('LabelShape', [('width', float), ('height', float)])
