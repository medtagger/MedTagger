"""Tests for Labels with Selections that have binary masks."""
import json
from typing import Any

from medtagger.database.models import LabelStatus

from tests.functional_tests import get_api_client
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_label_selection_binary_mask(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application for adding and verifying Labels with Selections that have binary masks."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Add Scan to the system
    payload = {'category': 'LUNGS', 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload),
                               headers={'content-type': 'application/json',
                                        'Authentication-Token': user_token})
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 2. Send Slices
    with open('example_data/example_scan/slice_1.dcm', 'rb') as image:
        response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
            'image': (image, 'slice_1.dcm'),
        }, content_type='multipart/form-data')
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    slice_id = json_response['slice_id']
    assert isinstance(slice_id, str)
    assert len(slice_id) >= 1

    # Step 3. Label it
    payload = {
        'selections': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'binary_mask': 'THIS_IS_BASE64_REPRESENTATION',
        }],
        'labeling_time': 34.56,
    }
    response = api_client.post('/api/v1/scans/{}/label'.format(scan_id), data=json.dumps(payload),
                               headers={'content-type': 'application/json', 'Authentication-Token': user_token})
    assert response.status_code == 201
    json_response = json.loads(response.data)
    label_id = json_response['label_id']

    # Step 4. Get random label for validation
    response = api_client.get('/api/v1/labels/random')
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['label_id'] == label_id
    assert json_response['labeling_time'] == 34.56
    assert json_response['status'] == LabelStatus.NOT_VERIFIED.value
    assert json_response['scan_id'] == scan_id
    assert json_response['selections'] == [{
        'x': 0.5,
        'y': 0.5,
        'slice_index': 0,
        'width': 0.1,
        'height': 0.1,
        'binary_mask': 'THIS_IS_BASE64_REPRESENTATION',
    }]
