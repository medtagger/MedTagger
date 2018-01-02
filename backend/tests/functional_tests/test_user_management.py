"""Tests for user management operations."""
import json
from typing import Any

from tests.functional_tests import get_api_client


def test_basic_user_flow(prepare_environment: Any) -> None:
    """Test for basic user flow"""
    api_client = get_api_client()
    email = 'test@mail.com'
    password = 'medtagger1'
    first_name = 'First'
    last_name = 'Last'

    # Step 1. User creates an account
    payload = {'email': email, 'password': password, 'firstName': first_name, 'lastName': last_name}
    response = api_client.post('/api/v1/account/register', data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    user_id = json_response['id']
    assert user_id == 1

    # Step 2. User logs in
    payload = {'email': email, 'password': password}
    response = api_client.post('/api/v1/account/sign-in', data=json.dumps(payload),
                               headers={'content-type': 'application/json'})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    user_token = json_response['token']
    assert isinstance(user_token, str)
    assert len(user_token) == 149

    # Step 3. Get user account information
    response = api_client.get('/api/v1/account/user-info', headers={'Authentication-Token': user_token})
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['id'] == 1
    assert json_response['email'] == email
    assert json_response['firstName'] == first_name
    assert json_response['lastName'] == last_name
    assert json_response['role'] == 'volunteer'

    # Step 4. User logs out
    response = api_client.post('/api/v1/account/sign-out', headers={'Authentication-Token': user_token})
    assert response.status_code == 204
