"""Unit tests for medtagger/api/scans/business.py."""
from typing import Any

import pytest

from medtagger.api.scans.business import add_label_element
from medtagger.api.exceptions import InvalidArgumentsException


def test_add_label_missing_tool(mocker: Any) -> None:
    """Check if method used by status endpoint has proper handling for missing tool in Label Elements."""
    element = {
        'x': 0.5,
        'y': 0.5,
        'slice_index': 0,
        'width': 0.1,
        'height': 0.1,
        'tag': 'LEFT_KIDNEY',
    }

    with pytest.raises(InvalidArgumentsException) as exception:
        add_label_element(element, label_id='12345')
    assert str(exception.value) == 'Tool is required!'

