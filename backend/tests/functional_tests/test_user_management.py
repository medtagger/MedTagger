"""Tests for user management operations."""
import json
from typing import Any

from tests.functional_tests import get_api_client
from medtagger.api.users.business import set_user_role
from medtagger.api.auth.business import create_user

example_user_email = 'test@mail.com'
example_user_password = 'medtagger1'
example_user_first_name = 'First'
example_user_last_name = 'Last'

admin_email = 'admin@medtagger.com'
admin_password = 'medtagger2'
admin_first_name = 'First'
admin_last_name = 'Last'


def test_basic_user_flow(prepare_environment: Any) -> None:
    """Test for basic user flow"""
    api_client = get_api_client()

    # Step 1. User creates an account
    payload = {'email': example_user_email, 'password': example_user_password,
               'firstName': example_user_first_name, 'lastName': example_user_last_name}
    response = api_client.post('/api/v1/auth/register', data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    user_id = json_response['id']
    assert user_id == 1

    # Step 2. User logs in
    payload = {'email': example_user_email, 'password': example_user_password}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    user_token = json_response['token']
    assert isinstance(user_token, str)
    assert len(user_token) == 149

    # Step 3. Get user account information
    response = api_client.get('/api/v1/users/info', headers={'Authentication-Token': user_token})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['id'] == 1
    assert json_response['email'] == example_user_email
    assert json_response['firstName'] == example_user_first_name
    assert json_response['lastName'] == example_user_last_name
    assert json_response['role'] == 'volunteer'

    # Step 4. User logs out
    response = api_client.post('/api/v1/auth/sign-out', headers={'Authentication-Token': user_token})
    assert response.status_code == 204


def test_upgrade_to_doctor_role(prepare_environment: Any) -> None:
    """Test for upgrading volunteer's to doctor's role"""
    api_client = get_api_client()

    admin_id = create_user(admin_email, admin_password, admin_first_name, admin_last_name)
    volunteer_id = create_user(example_user_email, example_user_password, example_user_first_name,
                               example_user_last_name)
    set_user_role(admin_id, 'admin')
    set_user_role(volunteer_id, 'volunteer')

    # Step 1. Admin user logs in
    payload = {'email': admin_email, 'password': admin_password}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    admin_user_token = json_response['token']
    assert isinstance(admin_user_token, str)
    assert len(admin_user_token) == 149

    # Step 2. Admin gets all users
    response = api_client.get('/api/v1/users/')
    print(response.data)
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    users = json_response['users']
    assert len(users) == 2

    # Step 3. Admin changes role for user
    payload = {'role': 'doctor'}
    response = api_client.put('/api/v1/users/{}/role'.format(volunteer_id), data=json.dumps(payload),
                              headers={'Authentication-Token': admin_user_token, 'content-type': 'application/json'})
    assert response.status_code == 204

    # Step 4. Admin logs out
    response = api_client.post('/api/v1/auth/sign-out', headers={'Authentication-Token': admin_user_token})
    assert response.status_code == 204

    # Step 5. User logs in
    payload = {'email': example_user_email, 'password': example_user_password}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    json_response = json.loads(response.data)
    user_token = json_response['token']
    assert response.status_code == 200

    # Step 6. Check if user role was changed
    response = api_client.get('/api/v1/users/info', headers={'Authentication-Token': user_token})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['role'] == 'doctor'
