"""Tests for basic flow of the system."""
import json
from typing import Any

from medtagger.definitions import LabelVerificationStatus, LabelElementStatus, LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    label_tags as LabelTagsRepository,
    tasks as TasksRepository,
)

from tests.functional_tests import get_api_client, get_web_socket_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


# pylint: disable=too-many-locals
def test_basic_flow(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application with basic flow."""
    api_client = get_api_client()
    web_socket_client = get_web_socket_client(namespace='/slices')
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], '', [], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)

    # Step 2. Get all datasets
    response = api_client.get('/api/v1/datasets', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, list)
    dataset = json_response[0]
    dataset_key = dataset['key']
    task_key = dataset['tasks'][0]['key']
    assert isinstance(dataset_key, str)
    assert len(dataset_key) > 1

    # Step 3. Add Scan to the system
    payload = {'dataset': dataset_key, 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id = json_response['scan_id']
    assert isinstance(scan_id, str)
    assert len(scan_id) >= 1

    # Step 4. Send slices
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

    # Step 5. Get random scan
    response = api_client.get('/api/v1/scans/random?task={}'.format(task_key),
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 1
    assert json_response['width'] == 512
    assert json_response['height'] == 512
    assert not json_response['predefined_label_id']

    # Step 6. Get slices from the server
    payload = {'scan_id': scan_id, 'task_key': task_key, 'begin': 0, 'count': 1}
    web_socket_client.emit('request_slices', payload, namespace='/slices')
    responses = web_socket_client.get_received(namespace='/slices')
    assert len(responses) == 1
    response = responses[0]
    assert response['name'] == 'slice'
    assert response['args'][0]['scan_id'] == scan_id
    assert response['args'][0]['index'] == 0
    assert isinstance(response['args'][0]['image'], bytes)

    # Step 7. Label it
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'EXAMPLE_TAG',
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

    # Step 8. Get random label for validation
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
    assert json_response['elements'][0]['tag'] == 'EXAMPLE_TAG'
    assert json_response['elements'][0]['tool'] == LabelTool.RECTANGLE.value
    assert json_response['elements'][0]['status'] == LabelElementStatus.NOT_VERIFIED.value

    # # Step 9. Verification of labels will be disabled until mechanism for validation of label elements is introduced
    # payload = {'status': LabelStatus.VALID.value}
    # response = api_client.put('/api/v1/labels/{}/status'.format(label_id), data=json.dumps(payload),
    #                           headers=get_headers(token=user_token, json=True))
    # assert response.status_code == 200
    # json_response = json.loads(response.data)
    # assert isinstance(json_response, dict)
    # assert json_response['label_id'] == label_id
    # assert json_response['status'] == LabelStatus.VALID.value
    #
    # # Step 10. Try to get another label for validation
    # response = api_client.get('/api/v1/labels/random', headers=get_headers(token=user_token))
    # assert response.status_code == 404


# pylint: disable=too-many-locals
def test_basic_flow_with_predefined_label(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application with basic flow that uses Predefined Label in Scan."""
    api_client = get_api_client()
    web_socket_client = get_web_socket_client(namespace='/slices')
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], '', [], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE, LabelTool.BRUSH], task.id)

    # Step 2. Get all datasets
    response = api_client.get('/api/v1/datasets', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, list)
    dataset = json_response[0]
    dataset_key = dataset['key']
    task_key = dataset['tasks'][0]['key']

    # Step 3. Add Scan to the system
    payload = {'dataset': dataset_key, 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id = json_response['scan_id']

    # Step 4. Send slices
    with open('tests/assets/example_scan/slice_1.dcm', 'rb') as image:
        response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
            'image': (image, 'slice_1.dcm'),
        }, content_type='multipart/form-data', headers=get_headers(token=user_token))
    assert response.status_code == 201

    # Step 5. Send Predefined Label
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.RECTANGLE.value,
        }, {
            'slice_index': 0,
            'width': 128,
            'height': 128,
            'image_key': 'SLICE_1',
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.BRUSH.value,
        }],
        'labeling_time': None,
    }
    with open('tests/assets/example_labels/binary_mask.png', 'rb') as image:
        data = {
            'label': json.dumps(payload),
            'SLICE_1': (image, 'slice_1'),
        }
        response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label?is_predefined=true'.format(scan_id),
                                   data=data, headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    predefined_label_id = json_response['label_id']
    assert type(predefined_label_id), str
    assert predefined_label_id

    # Step 6. Get random scan
    response = api_client.get('/api/v1/scans/random?task={}'.format(task_key),
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 1
    assert json_response['width'] == 512
    assert json_response['height'] == 512
    assert json_response['predefined_label_id'] == predefined_label_id

    # Step 7. Get slices from the server
    payload = {'scan_id': scan_id, 'task_key': task_key, 'begin': 0, 'count': 1}
    web_socket_client.emit('request_slices', payload, namespace='/slices')
    responses = web_socket_client.get_received(namespace='/slices')
    assert len(responses) == 2
    slice_response = next(response for response in responses if response['name'] == 'slice')
    assert slice_response['args'][0]['scan_id'] == scan_id
    assert slice_response['args'][0]['index'] == 0
    assert isinstance(slice_response['args'][0]['image'], bytes)
    brush_label_response = next(response for response in responses if response['name'] == 'brush_labels')
    assert brush_label_response['args'][0]['scan_id'] == scan_id
    assert brush_label_response['args'][0]['tag_key'] == 'EXAMPLE_TAG'
    assert brush_label_response['args'][0]['index'] == 0
    assert isinstance(brush_label_response['args'][0]['image'], bytes)

    # Step 8. Label it
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'EXAMPLE_TAG',
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

    # Step 9. Get random label for validation
    response = api_client.get('/api/v1/labels/random', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['label_id'] == label_id
