"""Module containing all custom types"""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)
LabelID = NewType('LabelID', int)

PickledDicomImage = NewType('PickledDicomImage', str)

CuboidLabelPosition = NamedTuple('CuboidLabelPosition', [('x', float), ('y', float), ('z', float)])
CuboidLabelShape = NamedTuple('CuboidLabelShape', [('width', float), ('height', float), ('depth', float)])
