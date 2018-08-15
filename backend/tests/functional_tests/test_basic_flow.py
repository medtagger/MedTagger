"""Tests for basic flow of the system."""
import json
from typing import Any

from medtagger.definitions import LabelVerificationStatus, LabelElementStatus, LabelTool
from tests.functional_tests import get_api_client, get_web_socket_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user
from tests.functional_tests.helpers import create_tag_and_assign_to_task


# pylint: disable=too-many-locals
def test_basic_flow(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application with basic flow."""
    api_client = get_api_client()
    web_socket_client = get_web_socket_client(namespace='/slices')
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Get all datasets
    response = api_client.get('/api/v1/scans/datasets', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, list)
    dataset = json_response[0]
    dataset_key = dataset['key']
    task_key = dataset['tasks'][0]['key']
    assert isinstance(dataset_key, str)
    assert len(dataset_key) > 1

    # Step 2. Add Scan to the system
    payload = {'dataset': dataset_key, 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id = json_response['scan_id']
    assert isinstance(scan_id, str)
    assert len(scan_id) >= 1

    # Step 3. Send slices
    with open('tests/assets/example_scan/slice_1.dcm', 'rb') as image:
        response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
            'image': (image, 'slice_1.dcm'),
        }, content_type='multipart/form-data', headers=get_headers(token=user_token))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    slice_id = json_response['slice_id']
    assert isinstance(slice_id, str)
    assert len(slice_id) >= 1

    # Step 4. Get random scan
    response = api_client.get('/api/v1/scans/random?task={}'.format(task_key),
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 1
    assert json_response['width'] == 512
    assert json_response['height'] == 512

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
    tag_key = 'EXAMPLE_TAG'
    create_tag_and_assign_to_task(tag_key, 'Example tag', task_key, [LabelTool.RECTANGLE])
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': tag_key,
            'tool': LabelTool.RECTANGLE.value,
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_id = json_response['label_id']
    assert isinstance(label_id, str)
    assert len(label_id) >= 1

    # Step 7. Get random label for validation
    response = api_client.get('/api/v1/labels/random', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['label_id'] == label_id
    assert json_response['labeling_time'] == 12.34
    assert json_response['status'] == LabelVerificationStatus.NOT_VERIFIED.value
    assert json_response['scan_id'] == scan_id
    assert len(json_response['elements'][0]['label_element_id']) >= 1
    assert json_response['elements'][0]['x'] == 0.5
    assert json_response['elements'][0]['y'] == 0.5
    assert json_response['elements'][0]['slice_index'] == 0
    assert json_response['elements'][0]['width'] == 0.1
    assert json_response['elements'][0]['height'] == 0.1
    assert json_response['elements'][0]['tag'] == tag_key
    assert json_response['elements'][0]['tool'] == LabelTool.RECTANGLE.value
    assert json_response['elements'][0]['status'] == LabelElementStatus.NOT_VERIFIED.value

    # # Step 8. Verification of labels will be disabled until mechanism for validation of label elements is introduced
    # payload = {'status': LabelStatus.VALID.value}
    # response = api_client.put('/api/v1/labels/{}/status'.format(label_id), data=json.dumps(payload),
    #                           headers=get_headers(token=user_token, json=True))
    # assert response.status_code == 200
    # json_response = json.loads(response.data)
    # assert isinstance(json_response, dict)
    # assert json_response['label_id'] == label_id
    # assert json_response['status'] == LabelStatus.VALID.value
    #
    # # Step 9. Try to get another label for validation
    # response = api_client.get('/api/v1/labels/random', headers=get_headers(token=user_token))
    # assert response.status_code == 404
