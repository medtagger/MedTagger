"""Tests for endpoints that checks status of the system"""
import json
from typing import Any

from tests.functional_tests import get_api_client


def test_status_endpoint(prepare_environment: Any) -> None:
    """Test for endpoint that checks status of the system"""
    api_client = get_api_client()

    response = api_client.get('/api/v1/core/status')
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert json_response == {'success': True}
