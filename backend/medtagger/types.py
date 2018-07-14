"""Module containing all custom types."""
from typing import NewType, NamedTuple


ScanID = NewType('ScanID', str)
SliceID = NewType('SliceID', str)
LabelID = NewType('LabelID', str)
LabelElementID = NewType('LabelElementID', str)
LabelTagID = NewType('LabelTagID', int)
PointID = NewType('PointID', str)

SliceLocation = NewType('SliceLocation', float)
SlicePosition = NamedTuple('SlicePosition', [('x', float), ('y', float), ('z', float)])

LabelPosition = NamedTuple('LabelPosition', [('x', float), ('y', float), ('slice_index', int)])
LabelShape = NamedTuple('LabelShape', [('width', float), ('height', float)])

Point = NamedTuple('Point', [('x', float), ('y', float)])

LabelingTime = NewType('LabelingTime', float)

ActionID = NewType('ActionID', int)
SurveyID = NewType('SurveyID', ActionID)
SurveyElementID = NewType('SurveyElementID', int)
SurveyElementKey = NewType('SurveyElementKey', str)
ActionResponseID = NewType('ActionResponseID', int)
SurveyResponseID = NewType('SurveyResponseID', ActionResponseID)
