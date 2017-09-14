"""Module containing all custom types"""
from typing import NewType, NamedTuple


ScanID = NewType('ScanId', int)
LabelID = NewType('LabelId', int)
UserId = NewType('UserId', int)

CuboidLabelPosition = NamedTuple('CuboidLabelPosition', [('x', float), ('y', float), ('z', float)])
CuboidLabelShape = NamedTuple('CuboidLabelShape', [('width', float), ('height', float), ('depth', float)])
