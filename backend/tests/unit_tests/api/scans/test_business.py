"""Unit tests for medtagger/api/scans/business.py."""
from typing import Any

import pytest

from medtagger.api.scans.business import add_label_element
from medtagger.api.exceptions import InvalidArgumentsException
from medtagger.database.models import LabelTool
from medtagger.types import LabelID


def test_add_label_element_tool_not_supported(mocker: Any) -> None:
    """Check if method for adding label elements used by add_label endpoint handles not supported tool."""
    element = {
        'x': 0.5,
        'y': 0.5,
        'slice_index': 0,
        'width': 0.1,
        'height': 0.1,
        'tag': 'LEFT_KIDNEY',
        'tool': 'NOT_SUPPORTED',
    }

    with pytest.raises(InvalidArgumentsException) as exception:
        add_label_element(element, LabelID('1234'))
    assert str(exception.value) == 'Tool is not supported!'


def test_add_label_element_missing_tool(mocker: Any) -> None:
    """Check if method for adding label elements used by add_label endpoint handles missing tool."""
    element = {
        'x': 0.5,
        'y': 0.5,
        'slice_index': 0,
        'width': 0.1,
        'height': 0.1,
        'tag': 'LEFT_KIDNEY',
    }

    with pytest.raises(InvalidArgumentsException) as exception:
        add_label_element(element, LabelID('1234'))
    assert str(exception.value) == 'Tool is required!'


def test_add_label_element_missing_tag(mocker: Any) -> None:
    """Check if method for adding label elements used by add_label endpoint handles for missing tag."""
    element = {
        'x': 0.5,
        'y': 0.5,
        'slice_index': 0,
        'width': 0.1,
        'height': 0.1,
        'tool': LabelTool.RECTANGLE.value,
    }

    with pytest.raises(InvalidArgumentsException) as exception:
        add_label_element(element, LabelID('1234'))
    assert str(exception.value) == 'Tag is required!'
