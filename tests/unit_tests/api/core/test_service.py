"""Unit tests for data_labeling/api/core/service.py"""
import json
from typing import Any

import pytest

from tests.unit_tests.api import get_test_application


@pytest.fixture
def success_fixture(mocker: Any) -> None:
    """Return fixture for success method used by status endpoint"""
    mocked_success = mocker.patch('data_labeling.api.core.service_rest.success')
    mocked_success.return_value = {'success': True}
    return mocked_success


def test_status_endpoint(mocker: Any, success_fixture: Any) -> None:
    """Check if status endpoint return data that was returned from business logic"""
    client = get_test_application(mocker)

    response = client.get('/api/v1/core/status')
    assert response.status_code == 200

    json_response = json.loads(response.data)
    assert json_response == {'success': True}
