"""Tests for user's settings."""
import json
from typing import Any

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.test_users import EXAMPLE_USER_EMAIL, EXAMPLE_USER_PASSWORD, EXAMPLE_USER_LAST_NAME, \
    EXAMPLE_USER_FIRST_NAME


def test_do_not_show_tutorial_again(prepare_environment: Any) -> None:
    """If user ends tutorial with "Do not show this tutorial again" checked, the user should not see tutorial again."""
    api_client = get_api_client()

    # Step 1. User creates an account
    payload = {'email': EXAMPLE_USER_EMAIL, 'password': EXAMPLE_USER_PASSWORD,
               'firstName': EXAMPLE_USER_FIRST_NAME, 'lastName': EXAMPLE_USER_LAST_NAME}
    api_client.post('/api/v1/auth/register', data=json.dumps(payload), headers=get_headers(json=True))

    # Step 2. User logs in
    payload = {'email': EXAMPLE_USER_EMAIL, 'password': EXAMPLE_USER_PASSWORD}
    response = api_client.post('/api/v1/auth/sign-in', data=json.dumps(payload),
                               headers=get_headers(json=True))
    user_token = json.loads(response.data)['token']

    # Step 3. Assure that parameter 'skipTutorial' in user's settings is False
    response = api_client.get('/api/v1/users/info', headers=get_headers(token=user_token))
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    user_id = json_response['id']
    assert json_response['settings']['skipTutorial'] is False

    # Step 4. Set 'skipTutorial' parameter to True
    payload = {'skipTutorial': True}
    response = api_client.post('/api/v1/users/' + str(user_id) + '/settings', data=json.dumps(payload),
                               headers=get_headers(json=True, token=user_token))
    assert response.status_code == 204

    # Step 5. Assure that parameter 'skipTutorial' in user's settings is True
    response = api_client.get('/api/v1/users/info', headers=get_headers(token=user_token))
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    assert json_response['settings']['skipTutorial'] is True
