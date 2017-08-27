"""Module containing all custom types"""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)

RectangleLabelPosition = NamedTuple('RectangleLabelPosition', [('x', float), ('y', float), ('z', float)])
RectangleLabelShape = NamedTuple('RectangleLabelShape', [('width', float), ('height', float), ('depth', float)])
