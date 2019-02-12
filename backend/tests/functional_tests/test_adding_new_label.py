"""Tests for adding new Labels to the system."""
import json
from typing import Any

from medtagger.storage import Storage
from medtagger.storage.models import BrushLabelElement
from medtagger.definitions import LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    label_tags as LabelTagsRepository,
    tasks as TasksRepository,
)

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_add_brush_label(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for adding a Label made with Brush tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')
    storage = Storage()

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.BRUSH], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Label it with Brush
    payload = {
        'elements': [{
            'slice_index': 0,
            'width': 128,
            'height': 128,
            'image_key': 'SLICE_1',
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.BRUSH.value,
        }],
        'labeling_time': 12.34,
        'task_id': TasksRepository.get_task_by_key('MARK_KIDNEYS').id,
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

    # Step 4. Fetch details about above Label and check image storage
    response = api_client.get('/api/v1/labels/' + label_id, headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_element_id = json_response['elements'][0]['label_element_id']
    brush_label_element = storage.get(BrushLabelElement, id=label_element_id)
    assert brush_label_element.image


def test_add_point_label(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for adding a Label made with Point tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.POINT], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Label it with Point Tool
    payload = {
        'elements': [{
            'slice_index': 0,
            'x': 0.25,
            'y': 0.5,
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.POINT.value,
        }],
        'labeling_time': 12.34,
    }
    data = {
        'label': json.dumps(payload),
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id), data=data,
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_id = json_response['label_id']
    assert isinstance(label_id, str)
    assert len(label_id) >= 1

    # Step 4. Fetch details about above Label
    response = api_client.get('/api/v1/labels/' + label_id, headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert len(json_response['elements']) == 1
    assert json_response['elements'][0]['x'] == 0.25
    assert json_response['elements'][0]['y'] == 0.5


def test_add_chain_label(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for adding a Label made with Chain tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.CHAIN], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Label it with Chain Tool
    payload = {
        'elements': [{
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
    data = {
        'label': json.dumps(payload),
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id), data=data,
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_id = json_response['label_id']
    assert isinstance(label_id, str)
    assert len(label_id) >= 1

    # Step 4. Fetch details about above Label
    response = api_client.get('/api/v1/labels/' + label_id, headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert len(json_response['elements']) == 1
    assert json_response['elements'][0]['points'][0]['x'] == 0.2
    assert json_response['elements'][0]['points'][0]['y'] == 0.3
    assert json_response['elements'][0]['points'][1]['x'] == 0.5
    assert json_response['elements'][0]['points'][1]['y'] == 0.8
    assert not json_response['elements'][0]['loop']


def test_add_chain_label_not_enough_points(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for adding a Label made with Chain tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.CHAIN], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Label it with Chain Tool
    payload = {
        'elements': [{
            'slice_index': 0,
            'points': [
                {
                    'x': 0.2,
                    'y': 0.3,
                },
            ],
            'tag': 'EXAMPLE_TAG',
            'tool': LabelTool.CHAIN.value,
            'loop': False,
        }],
        'labeling_time': 12.34,
    }
    data = {
        'label': json.dumps(payload),
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id), data=data,
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400


def test_add_label_with_tag_from_other_task(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for adding a Label with Tag from other Task."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    left_task = TasksRepository.add_task('MARK_LEFT', 'Mark Left', 'path/to/image', ['KIDNEYS'], [])
    right_task = TasksRepository.add_task('MARK_RIGHT', 'Mark Left', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('TAG_LEFT', 'Tag Left', [LabelTool.POINT], left_task.id)
    LabelTagsRepository.add_new_tag('TAG_RIGHT', 'Tag Right', [LabelTool.POINT], right_task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Label it with an element with Tag from another Task
    payload = {
        'elements': [{
            'slice_index': 0,
            'x': 0.25,
            'y': 0.5,
            'tag': 'TAG_RIGHT',
            'tool': LabelTool.POINT.value,
        }],
        'labeling_time': 12.34,
    }
    data = {
        'label': json.dumps(payload),
    }
    response = api_client.post('/api/v1/scans/{}/MARK_LEFT/label'.format(scan_id), data=data,
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['message'] == 'Invalid arguments.'
    assert json_response['details'] == 'Tag TAG_RIGHT is not part of Task MARK_LEFT.'
