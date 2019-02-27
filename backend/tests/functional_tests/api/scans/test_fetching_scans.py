"""Tests for REST API for fetching metadata about Scans."""
import json
from typing import Any

from medtagger.repositories import (
    datasets as DatasetsRepository,
    scans as ScansRepository,
)

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_get_paginated_scans(prepare_environment: Any) -> None:
    """Test for fetching Scans in the paginated way."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')

    # Step 2. Add example Scans to the system
    for _ in range(50):
        ScansRepository.add_new_scan(dataset, number_of_slices=3)

    # Step 3. Fetch them with MedTagger REST API
    response = api_client.get('/api/v1/scans?dataset_key=KIDNEYS', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert json_response['pagination']['page'] == 1
    assert json_response['pagination']['per_page'] == 25
    assert json_response['pagination']['total'] == 50
    assert len(json_response['scans']) == 25

    # Step 4. Fetch the next page with different size
    response = api_client.get('/api/v1/scans?dataset_key=KIDNEYS&page=2&per_page=10',
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert json_response['pagination']['page'] == 2
    assert json_response['pagination']['per_page'] == 10
    assert json_response['pagination']['total'] == 50
    assert len(json_response['scans']) == 10


def test_get_paginated_scans_by_volunteer(prepare_environment: Any) -> None:
    """Test for fetching Scans in the paginated way by volunteers."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('volunteer')

    # Step 1. Prepare a structure for the test
    dataset = DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')

    # Step 2. Add example Scans to the system
    for _ in range(50):
        ScansRepository.add_new_scan(dataset, number_of_slices=3)

    # Step 3. Fetch them with MedTagger REST API
    response = api_client.get('/api/v1/scans?dataset_key=KIDNEYS', headers=get_headers(token=user_token))
    assert response.status_code == 403
    json_response = json.loads(response.data)
    assert json_response['message'] == 'Access forbidden'
    assert json_response['details'] == 'You don\'t have required roles to access this method.'
