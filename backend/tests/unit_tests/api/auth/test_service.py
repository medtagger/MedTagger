"""Unit tests for medtagger/api/auth/service.py."""
from typing import Any

import pytest
from flask import json

from medtagger.api import InvalidArgumentsException
from tests.unit_tests.api import get_test_application


@pytest.fixture
def create_user_exception_fixture(mocker: Any) -> None:
    """Return fixture for create user method used by create user endpoint."""
    mocked_create_user_failure = mocker.patch('medtagger.api.auth.service.create_user')
    mocked_create_user_failure.side_effect = InvalidArgumentsException('User with this email already exist')
    return mocked_create_user_failure


@pytest.fixture
def sign_in_wrong_password_fixture(mocker: Any) -> None:
    """Return fixture for sing in user method used by sing in endpoint."""
    mocked_sign_in_failure = mocker.patch('medtagger.api.auth.service.sign_in_user')
    mocked_sign_in_failure.side_effect = InvalidArgumentsException('Password does not match.')
    return mocked_sign_in_failure


def test_create_user_user_already_exist(mocker: Any, create_user_exception_fixture: Any):
    """Check if create user endpoint responds accordingly to situation when user exists."""
    api = get_test_application(mocker)
    payload = {'email': 'test@mail.com', 'password': 'medtagger',
               'firstName': 'First', 'lastName': 'Last'}

    response = api.post('/api/v1/auth/register', data=json.dumps(payload), headers={'content-type': 'application/json'})

    json_response = json.loads(response.data)
    details = json_response['details']
    message = json_response['message']

    assert response.status_code == 400
    assert isinstance(json_response, dict)
    assert details == 'User with this email already exist'
    assert message == 'Invalid arguments.'


def test_create_user_password_too_short(mocker: Any):
    """Check if create user endpoint responds accordingly to wrong input (password too short)."""
    api = get_test_application(mocker)
    payload = {'email': 'test@mail.com', 'password': 'medtag',
               'firstName': 'First', 'lastName': 'Last'}

    response = api.post('/api/v1/auth/register', data=json.dumps(payload), headers={'content-type': 'application/json'})

    json_response = json.loads(response.data)
    errors = json_response['errors']
    message = json_response['message']

    assert response.status_code == 400
    assert isinstance(json_response, dict)
    assert errors == {'password': "'medtag' is too short"}
    assert message == 'Input payload validation failed'


def test_create_user_one_argument_missing(mocker: Any):
    """Check if create user endpoint responds accordingly to wrong input (missing email)."""
    api = get_test_application(mocker)
    payload = {'password': 'medtagger1', 'firstName': 'First', 'lastName': 'Last'}

    response = api.post('/api/v1/auth/register', data=json.dumps(payload), headers={'content-type': 'application/json'})

    json_response = json.loads(response.data)
    errors = json_response['errors']
    message = json_response['message']

    assert response.status_code == 400
    assert isinstance(json_response, dict)
    assert errors == {'email': "'email' is a required property"}
    assert message == 'Input payload validation failed'


def test_sing_in_wrong_password(mocker: Any, sign_in_wrong_password_fixture: Any):
    """Check if sign in endpoint responds accordingly to user providing wrong password."""
    api = get_test_application(mocker)
    payload = {'email': 'test@mail.com', 'password': 'medtaggger'}

    response = api.post('/api/v1/auth/sign-in', data=json.dumps(payload), headers={'content-type': 'application/json'})

    json_response = json.loads(response.data)
    details = json_response['details']
    message = json_response['message']

    assert response.status_code == 400
    assert isinstance(json_response, dict)
    assert details == 'Password does not match.'
    assert message == 'Invalid arguments.'
