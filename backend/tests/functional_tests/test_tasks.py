"""Tests for management of Tasks."""
import json
from typing import Any

from medtagger.repositories import datasets as DatasetsRepository

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_add_task(prepare_environment: Any) -> None:
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
    assert json_response['description'] == 'This task will focus on tagging nodules.'
    assert len(json_response['label_examples']) == 2
    assert len(json_response['tags']) == 2
    assert len(json_response['datasets_keys']) == 2

    # Step 3. Check for available Datasets through the REST API
    response = api_client.get('/api/v1/datasets', headers=get_headers(token=user_token, json=True))
    json_response = json.loads(response.data)
    datasets = [dataset for dataset in json_response
                if any(task for task in dataset['tasks'] if task['key'] == 'MARK_NODULES')]
    assert len(datasets) == 2

#
# def test_get_metadata(prepare_environment: Any) -> None:
#     """Test basic flow for retrieving metadata for Task"""
#
#     api_client = get_api_client()
#     user_token = get_token_for_logged_in_user('admin')
#
#     # Step 1. Prepare a structure for the test
#     DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
#     task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
#     LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)
#
#     # Step 2. Get all datasets
#     response = api_client.get('/api/v1/datasets', headers=get_headers(token=user_token))
#     assert response.status_code == 200
#     json_response = json.loads(response.data)
#     assert isinstance(json_response, list)
#     dataset = json_response[0]
#     dataset_key = dataset['key']
#     task_key = dataset['tasks'][0]['key']
#     assert isinstance(dataset_key, str)
#     assert len(dataset_key) > 1
#
#     # Step 3. Add Scan to the system
#     payload = {'dataset': dataset_key, 'number_of_slices': 1}
#     response = api_client.post('/api/v1/scans', data=json.dumps(payload),
#                                headers=get_headers(token=user_token, json=True))
#     assert response.status_code == 201
#     json_response = json.loads(response.data)
#     assert isinstance(json_response, dict)
#     scan_id = json_response['scan_id']
#     assert isinstance(scan_id, str)
#     assert len(scan_id) >= 1
#
#     # Step 4. Send slices
#     with open('tests/assets/example_scan/slice_1.dcm', 'rb') as image:
#         response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
#             'image': (image, 'slice_1.dcm'),
#         }, content_type='multipart/form-data', headers=get_headers(token=user_token))
#     assert response.status_code == 201
#     json_response = json.loads(response.data)
#     assert isinstance(json_response, dict)
#     slice_id = json_response['slice_id']
#     assert isinstance(slice_id, str)
#     assert len(slice_id) >= 1