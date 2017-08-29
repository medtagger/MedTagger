"""Module containing all custom types"""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', int)
LabelID = NewType('LabelID', int)

CuboidLabelPosition = NamedTuple('CuboidLabelPosition', [('x', float), ('y', float), ('z', float)])
CuboidLabelShape = NamedTuple('CuboidLabelShape', [('width', float), ('height', float), ('depth', float)])
