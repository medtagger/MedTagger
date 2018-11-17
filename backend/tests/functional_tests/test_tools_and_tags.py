"""Tests for operations of creating labels with tags and tools."""

from typing import Any

from flask import json

from medtagger.definitions import LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    label_tags as LabelTagsRepository,
    tasks as TasksRepository,
)

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


def test_add_label_non_existing_tag(prepare_environment: Any) -> None:
    """Test application for situation when users provides non existing tag."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('LEFT_KIDNEY', 'Left Kidney', [LabelTool.RECTANGLE], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Create label
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'NON_EXISTING',
            'tool': LabelTool.RECTANGLE.value,
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400
    json_response = json.loads(response.data)
    assert json_response['details'] == 'Tag NON_EXISTING is not part of Task MARK_KIDNEYS.'


def test_add_label_non_supported_tool(prepare_environment: Any) -> None:
    """Test application for situation when users provides non existing tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('LEFT_KIDNEY', 'Left Kidney', [LabelTool.RECTANGLE], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Create label
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'LEFT_KIDNEY',
            'tool': 'NON_EXISTING',
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400
    # [Related #288] Please fix this details message!
    # json_response = json.loads(response.data)
    # assert json_response['details'] == "'NON_EXISTING' is not one of ['RECTANGLE']"


def test_add_label_missing_tag(prepare_environment: Any) -> None:
    """Test application for situation when users does not provide tag."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('LEFT_KIDNEY', 'Left Kidney', [LabelTool.RECTANGLE], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Create label
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tool': LabelTool.RECTANGLE.value,
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400
    # [Related #288] Please fix this details message!
    # json_response = json.loads(response.data)
    # assert json_response['details'] == "'tag' is a required property"


def test_add_label_missing_tool(prepare_environment: Any) -> None:
    """Test application for situation when users does not provide tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('LEFT_KIDNEY', 'Left Kidney', [LabelTool.RECTANGLE], task.id)

    # Step 2. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Create label
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'LEFT_KIDNEY',
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400
    # [Related #288] Please fix this details message!
    # json_response = json.loads(response.data)
    # assert json_response['details'] == "'tool' is a required property"


def test_add_label_wrong_tool_for_tag(prepare_environment: Any) -> None:
    """Test application for situation when user creates a label with tool that is not available for given tag."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('KIDNEYS', 'Kidneys')
    task = TasksRepository.add_task('MARK_KIDNEYS', 'Mark Kidneys', 'path/to/image', ['KIDNEYS'], [])
    LabelTagsRepository.add_new_tag('LEFT_KIDNEY', 'Left Kidney', [LabelTool.RECTANGLE], task.id)

    # Step 1. Add Scan to the system
    payload = {'dataset': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 2. Create label
    payload = {
        'elements': [{
            'x': 0.5,
            'y': 0.5,
            'slice_index': 0,
            'width': 0.1,
            'height': 0.1,
            'tag': 'LEFT_KIDNEY',
            'tool': LabelTool.BRUSH.value,
        }],
        'labeling_time': 12.34,
    }
    response = api_client.post('/api/v1/scans/{}/MARK_KIDNEYS/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 400
