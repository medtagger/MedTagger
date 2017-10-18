"""Module containing all custom types"""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)
SliceID = NewType('SliceID', str)
LabelID = NewType('LabelID', int)

SliceLocation = NewType('SliceLocation', float)
SlicePosition = NamedTuple('SlicePosition', [('x', float), ('y', float), ('z', float)])

PickledDicomImage = NewType('PickledDicomImage', str)

CuboidLabelPosition = NamedTuple('CuboidLabelPosition', [('x', float), ('y', float), ('z', float)])
CuboidLabelShape = NamedTuple('CuboidLabelShape', [('width', float), ('height', float), ('depth', float)])
