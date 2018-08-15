"""Tests for management of Tasks."""
import json
from typing import Any

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_add_task(prepare_environment: Any) -> None:
    """Test application with basic flow."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    payload = {
        'key': 'MARK_NODULES',
        'name': 'Mark nodules',
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
    assert len(json_response['tags']) == 2

    response = api_client.get('/api/v1/scans/datasets', headers=get_headers(token=user_token, json=True))
    json_response = json.loads(response.data)
    datasets = [dataset for dataset in json_response
                if any(task for task in dataset['tasks'] if task['key'] == 'MARK_NODULES')]
    assert len(datasets) == 2
