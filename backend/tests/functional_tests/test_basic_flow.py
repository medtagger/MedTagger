"""Tests for basic flow of the system."""
import json
import pytest
from typing import Any

from medtagger.database.models import User, LabelStatus
from medtagger.repositories.users import UsersRepository
from tests.functional_tests import get_api_client, get_web_socket_client


@pytest.fixture
def user_repository_mock(mocker: Any) -> None:
    """Return user with volunteer role."""
    mocked_user_repository = mocker.patch('medtagger.api.users.get_user_by_id')
    mocked_user_repository.return_value = User('test@mail.com', 'medtagger', 'First', 'Last')
    return mocked_user_repository


def tqest_basic_flow(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application with basic flow."""
    api_client = get_api_client()
    web_socket_client = get_web_socket_client(namespace='/slices')

    # Step 1. Get all categories
    response = api_client.get('/api/v1/scans/categories')
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, list)
    category = json_response[0]
    category_key = category['key']
    assert isinstance(category_key, str)
    assert len(category_key) > 1

    # Step 2. Add Scan to the system
    payload = {'category': category_key, 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload), headers={'content-type': 'application/json'})
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id = json_response['scan_id']
    assert isinstance(scan_id, str)
    assert len(scan_id) >= 1

    # Step 3. Send slices
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

    # Step 4. Get random scan
    response = api_client.get('/api/v1/scans/random?category={}'.format(category_key))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 1

    # Step 5. Get slices from the server
    web_socket_client.emit('request_slices', {'scan_id': scan_id, 'begin': 0, 'count': 1}, namespace='/slices')
    responses = web_socket_client.get_received(namespace='/slices')
    assert len(responses) == 1
    response = responses[0]
    assert response['name'] == 'slice'
    assert response['args'][0]['scan_id'] == scan_id
    assert response['args'][0]['index'] == 0
    assert isinstance(response['args'][0]['image'], bytes)

    # Step 6. Label it
    payload = {
        'selections': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/label'.format(scan_id), data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_id = json_response['label_id']
    assert isinstance(label_id, str)
    assert len(label_id) >= 1

    # Step 7. Get random label for validation
    response = api_client.get('/api/v1/labels/random')
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['label_id'] == label_id
    assert json_response['labeling_time'] == 12.34
    assert json_response['status'] == LabelStatus.NOT_VERIFIED.value
    assert json_response['scan_id'] == scan_id
    assert json_response['selections'] == [{
        'x': 0.5,
        'y': 0.5,
        'slice_index': 0,
        'width': 0.1,
        'height': 0.1,
        'binary_mask': None,
    }]

    # Step 8. Verify such label
    payload = {'status': LabelStatus.VALID.value}
    response = api_client.put('/api/v1/labels/{}/status'.format(label_id), data=json.dumps(payload),
                              headers={'content-type': 'application/json'})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['label_id'] == label_id
    assert json_response['status'] == LabelStatus.VALID.value

    # Step 9. Try to get another label for validation
    response = api_client.get('/api/v1/labels/random')
    assert response.status_code == 404
