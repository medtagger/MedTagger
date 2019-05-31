"""Tests for deleting scans and its elements from database."""
import json
from typing import Any

from cassandra.cqlengine.query import DoesNotExist
from sqlalchemy.orm.exc import NoResultFound
import pytest

from medtagger.definitions import LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    label_tags as LabelTagsRepository,
    tasks as TasksRepository,
    scans as ScansRepository,
    slices as SliceRepository,
)
from medtagger.types import ScanID, SliceID
from medtagger.storage.models import BrushLabelElement, OriginalSlice, ProcessedSlice
from tests.functional_tests import get_api_client, get_web_socket_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_delete_scan_without_slices(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test deleting scan without any slices."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], '', [], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 0}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id: ScanID = json_response['scan_id']
    assert isinstance(scan_id, str)
    assert len(scan_id) >= 1

    # Step 3. Get scan
    response = api_client.get('/api/v1/scans/{}'.format(scan_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 0

    # Step 4. Delete scan from the system
    ScansRepository.delete_scan_by_id(scan_id)

    # Step 5. Check that scan has been deleted
    response = api_client.get('/api/v1/scans/{}'.format(scan_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 404


def test_delete_scan_with_slices(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test deleting scan with at least 1 slice."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], '', [], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id: ScanID = json_response['scan_id']
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
    slice_id: SliceID = json_response['slice_id']
    assert isinstance(slice_id, str)
    assert len(slice_id) >= 1

    # Step 4. Get scan
    response = api_client.get('/api/v1/scans/{}'.format(scan_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 1
    assert json_response['width'] == 512
    assert json_response['height'] == 512

    # Step 5. Delete scan from the system
    ScansRepository.delete_scan_by_id(scan_id)

    # Step 6. Check that scan has been deleted
    response = api_client.get('/api/v1/scans/{}'.format(scan_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 404

    # Step 7. Check that slices has been deleted
    with pytest.raises(NoResultFound):
        SliceRepository.get_slice_by_id(slice_id)


# pylint: disable=too-many-locals
def test_delete_scan_with_labels(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test deleting scan with at least 1 slice and with labels made with all tools."""
    api_client = get_api_client()
    web_socket_client = get_web_socket_client(namespace='/slices')
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], '', [], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag',
                                    [LabelTool.RECTANGLE, LabelTool.CHAIN, LabelTool.POINT, LabelTool.BRUSH],
                                    task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    scan_id: ScanID = json_response['scan_id']
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
    slice_id: SliceID = json_response['slice_id']
    assert isinstance(slice_id, str)
    assert len(slice_id) >= 1

    # Step 4. Get scan
    response = api_client.get('/api/v1/scans/{}'.format(scan_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['scan_id'] == scan_id
    assert json_response['number_of_slices'] == 1
    assert json_response['width'] == 512
    assert json_response['height'] == 512

    # Step 5. Get slices from the server
    payload = {'scan_id': scan_id, 'task_key': 'MARK_KIDNEYS', 'begin': 0, 'count': 1}
    web_socket_client.emit('request_slices', payload, namespace='/slices')
    responses = web_socket_client.get_received(namespace='/slices')
    assert len(responses) == 1
    response = responses[0]
    assert response['name'] == 'slice'
    assert response['args'][0]['scan_id'] == scan_id
    assert response['args'][0]['index'] == 0
    assert isinstance(response['args'][0]['image'], bytes)

    # Step 6. Label it with all available tools
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
        }, {
            'slice_index': 0,
            'x': 0.25,
            'y': 0.5,
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.POINT.value,
        }, {
            'slice_index': 0,
            'points': [
                {
                    'x': 0.2,
                    'y': 0.3,
                },
                {
                    'x': 0.5,
                    'y': 0.8,
                },
            ],
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.CHAIN.value,
            'loop': False,
        }],
        'labeling_time': 12.34,
    }
    with open('tests/assets/example_labels/binary_mask.png', 'rb') as image:
        data = {
            'label': json.dumps(payload),
            'SLICE_1': (image, 'slice_1'),
        }
        response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id), data=data,
                                   headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_id = json_response['label_id']
    assert isinstance(label_id, str)
    assert len(label_id) >= 1

    # Step 7. Fetch details about above Label and check image storage
    response = api_client.get('/api/v1/labels/' + label_id, headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_element_id = json_response['elements'][1]['label_element_id']
    brush_label_element = BrushLabelElement.get(id=label_element_id)
    assert brush_label_element.image

    # Step 7. Delete scan from the system
    ScansRepository.delete_scan_by_id(scan_id)

    # Step 8. Check that scan has been deleted
    response = api_client.get('/api/v1/scans/{}'.format(scan_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 404

    # Step 9. Check that slices has been deleted
    with pytest.raises(NoResultFound):
        SliceRepository.get_slice_by_id(slice_id)

    # Step 10. Check that slices original image has been deleted from storage
    with pytest.raises(DoesNotExist):
        OriginalSlice.get(id=slice_id)

    # Step 11. Check that slices processed image has been deleted from storage
    with pytest.raises(DoesNotExist):
        ProcessedSlice.get(id=slice_id)

    # Step 12. Check that labels has been deleted
    response = api_client.get('/api/v1/labels/{}'.format(label_id),
                              headers=get_headers(token=user_token))
    assert response.status_code == 404

    # Step 13. Check that Brush Label was deleted from storage
    with pytest.raises(DoesNotExist):
        BrushLabelElement.get(id=label_element_id)
