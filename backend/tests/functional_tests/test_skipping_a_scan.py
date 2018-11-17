"""Tests for skipping a scan."""
import json
from typing import Any

from medtagger.repositories import datasets as DatasetsRepository

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_skipping_a_scan(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for skipping a scan."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Skip Scan
    response = api_client.post('/api/v1/scans/' + scan_id + '/skip', headers=get_headers(token=user_token))
    assert response.status_code == 200


def test_skipping_a_scan_that_doesnt_exist(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for trying to skip a scan that doesn't exist."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')
    scan_id = 'EXAMPLE_SCAN_ID'

    # Step 1. Try to skip Scan.
    response = api_client.post('/api/v1/scans/' + scan_id + '/skip', headers=get_headers(token=user_token))
    assert response.status_code == 404
