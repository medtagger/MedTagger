"""Tests for management of Tasks."""
import glob
import json
from typing import Any

from medtagger.repositories import (
    datasets as DatasetsRepository,
)

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_add_task(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application with basic flow."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    DatasetsRepository.add_new_dataset('LUNGS', 'Lungs')

    # Step 2. Add new Task through the REST API
    payload = {
        'key': 'MARK_NODULES',
        'name': 'Mark nodules',
        'description': 'This task will focus on tagging nodules.',
        'label_examples': ['assets/labels/label_1.png', 'assets/labels/label_2.png'],
        'image_path': 'assets/icon/my_icon.svg',
        'datasets_keys': ['KIDNEYS', 'LUNGS'],
        'tags': [{
            'key': 'SMALL_NODULE',
            'name': 'Small nodule',
            'tools': ['POINT'],
        }, {
            'key': 'BIG_NODULE',
            'name': 'Big nodule',
            'tools': ['RECTANGLE', 'BRUSH'],
        }],
    }
    response = api_client.post('/api/v1/tasks', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['key'] == 'MARK_NODULES'
    assert json_response['name'] == 'Mark nodules'
    assert json_response['image_path'] == 'assets/icon/my_icon.svg'
    assert json_response['number_of_available_scans'] == 0
    assert len(json_response['label_examples']) == 2
    assert json_response['description'] == 'This task will focus on tagging nodules.'
    assert len(json_response['tags']) == 2
    assert len(json_response['datasets_keys']) == 2

    # Step 3. Check for available Datasets through the REST API
    response = api_client.get('/api/v1/datasets', headers=get_headers(token=user_token, json=True))
    json_response = json.loads(response.data)
    datasets = [dataset for dataset in json_response
                if any(task for task in dataset['tasks'] if task['key'] == 'MARK_NODULES')]
    assert len(datasets) == 2

    # Step 4. Add Scans to datasets
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']
    payload = {'dataset': 'LUNGS', 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201

    # Step 3. Send Slices
    for file in glob.glob('tests/assets/example_scan/*.dcm'):
        with open(file, 'rb') as image:
            response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
                'image': (image, 'slice_1.dcm'),
            }, headers=get_headers(token=user_token, multipart=True))
            assert response.status_code == 201

    # Step 4. Check for Task metadata through the REST API
    response = api_client.get('/api/v1/tasks/MARK_NODULES', headers=get_headers(token=user_token, json=True))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['key'] == 'MARK_NODULES'
    assert json_response['name'] == 'Mark nodules'
    assert json_response['number_of_available_scans'] == 1
    assert len(json_response['label_examples']) == 2
    assert json_response['description'] == 'This task will focus on tagging nodules.'
