"""Tests for user management operations."""
import json
from typing import Dict, Any

from medtagger.api.auth.business import create_user
from medtagger.api.users.business import set_user_role
from medtagger.definitions import LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    label_tags as LabelTagsRepository,
    tasks as TasksRepository,
)
from tests.functional_tests import get_api_client, get_headers

EXAMPLE_USER_EMAIL = 'test@mail.com'
EXAMPLE_USER_PASSWORD = 'medtagger1'
EXAMPLE_USER_FIRST_NAME = 'First'
EXAMPLE_USER_LAST_NAME = 'Last'

ADMIN_EMAIL = 'admin@medtagger.com'
ADMIN_PASSWORD = 'medtagger2'
ADMIN_FIRST_NAME = 'First'
ADMIN_LAST_NAME = 'Last'


def test_basic_user_flow(prepare_environment: Any) -> None:
    """Test for basic user flow."""
    api_client = get_api_client()

    # Step 1. User creates an account
    payload = {'email': EXAMPLE_USER_EMAIL, 'password': EXAMPLE_USER_PASSWORD,
               'firstName': EXAMPLE_USER_FIRST_NAME, 'lastName': EXAMPLE_USER_LAST_NAME}
    response = api_client.post('/api/v1/auth/register', data=json.dumps(payload),
                               headers=get_headers(json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    user_token = json_response['token']
    assert isinstance(user_token, str)
    assert len(user_token) > 100

    # Step 3. Get user account information
    response = api_client.get('/api/v1/users/info', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['id'] > 0
    assert json_response['email'] == EXAMPLE_USER_EMAIL
    assert json_response['firstName'] == EXAMPLE_USER_FIRST_NAME
    assert json_response['lastName'] == EXAMPLE_USER_LAST_NAME
    assert json_response['role'] == 'volunteer'


def test_upgrade_to_doctor_role(prepare_environment: Any) -> None:
    """Test for upgrading volunteer's to doctor's role."""
    api_client = get_api_client()

    admin_id, _ = create_user(ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_FIRST_NAME, ADMIN_LAST_NAME)
    volunteer_id, _ = create_user(EXAMPLE_USER_EMAIL, EXAMPLE_USER_PASSWORD, EXAMPLE_USER_FIRST_NAME,
                                  EXAMPLE_USER_LAST_NAME)

    set_user_role(admin_id, 'admin')
    set_user_role(volunteer_id, 'volunteer')

    # Step 1. Admin user logs in
    payload = {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers=get_headers(json=True))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    admin_user_token = json_response['token']
    assert isinstance(admin_user_token, str)
    assert len(admin_user_token) > 100

    # Step 2. Admin gets all users
    response = api_client.get('/api/v1/users', headers=get_headers(token=admin_user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    users = json_response['users']
    assert len(users) == 2

    # Step 3. Admin changes role for user
    payload = {'role': 'doctor'}
    response = api_client.put('/api/v1/users/{}/role'.format(volunteer_id), data=json.dumps(payload),
                              headers=get_headers(token=admin_user_token, json=True))
    assert response.status_code == 200

    # Step 4. User logs in
    payload = {'email': EXAMPLE_USER_EMAIL, 'password': EXAMPLE_USER_PASSWORD}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers=get_headers(json=True))
    json_response = json.loads(response.data)
    user_token = json_response['token']
    assert response.status_code == 200

    # Step 5. Check if user role was changed
    response = api_client.get('/api/v1/users/info', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['role'] == 'doctor'


def test_ownership(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for checking scan and label ownership."""
    api_client = get_api_client()

    # Step 1. Prepare a structure for the test
    DatasetsRepository.add_new_dataset('LUNGS', 'Lungs')
    task = TasksRepository.add_task('FIND_NODULES', 'Find Nodules', 'path/to/image', ['LUNGS'], '', [], [])
    LabelTagsRepository.add_new_tag('EXAMPLE_TAG', 'Example Tag', [LabelTool.RECTANGLE], task.id)
    admin_id, _ = create_user(ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_FIRST_NAME, ADMIN_LAST_NAME)
    set_user_role(admin_id, 'admin')

    # Step 2. Admin user logs in
    payload: Dict[str, Any] = {'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers=get_headers(json=True))
    json_response = json.loads(response.data)
    admin_user_token = json_response['token']
    assert response.status_code == 200

    # Step 3. Add Scan to the system
    payload = {'dataset': 'LUNGS', 'number_of_slices': 1}
    response = api_client.post('/api/v1/scans', data=json.dumps(payload),
                               headers=get_headers(token=admin_user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    owner_id = json_response['owner_id']
    assert owner_id == admin_id
    scan_id = json_response['scan_id']

    # Step 4. Send slices
    with open('tests/assets/example_scan/slice_1.dcm', 'rb') as image:
        response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
            'image': (image, 'slice_1.dcm'),
        }, content_type='multipart/form-data', headers=get_headers(token=admin_user_token))
    assert response.status_code == 201

    # Step 5. Label
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
    response = api_client.post('/api/v1/scans/{}/FIND_NODULES/label'.format(scan_id),
                               data={'label': json.dumps(payload)},
                               headers=get_headers(token=admin_user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    owner_id = json_response['owner_id']
    assert owner_id == admin_id
