"""Unit tests for medtagger/api/auth/business.py."""
from typing import Any

import pytest

from medtagger.api import InvalidArgumentsException
from medtagger.database.models import User
from medtagger.repositories.users import UsersRepository
from medtagger.repositories.roles import RolesRepository
from medtagger.api.auth.business import create_user
from medtagger.api.auth.business import sign_in_user


@pytest.fixture
def get_user_by_email_success_fixture(mocker: Any) -> None:
    """Return fixture for get user by email method used in create user business method."""
    mocked_user_repository = mocker.patch.object(UsersRepository, 'get_user_by_email')
    mocked_user_repository.return_value = User('test@mail.com', 'medtagger', 'First', 'Last')
    return mocked_user_repository


@pytest.fixture
def get_user_by_email_failure_fixture(mocker: Any) -> None:
    """Return fixture for get user by email method used in create user business method."""
    mocked_user_repository = mocker.patch.object(UsersRepository, 'get_user_by_email')
    mocked_user_repository.return_value = None
    return mocked_user_repository


@pytest.fixture
def get_role_fixture(mocker: Any) -> None:
    """Return fixture for get role with name method used in create user business method."""
    mocked_roles_repository = mocker.patch.object(RolesRepository, 'get_role_with_name')
    mocked_roles_repository.return_value = None
    return mocked_roles_repository


@pytest.fixture
def wrong_password_fixture(mocker: Any) -> None:
    """Return fixture for get role with namem ethod used in create user business method."""
    mocked_check_password = mocker.patch('medtagger.api.auth.business.check_password_hash')
    mocked_check_password.return_value = False
    return mocked_check_password


def test_create_user_user_exists(mocker: Any, get_user_by_email_success_fixture: Any) -> None:
    """Check if create user method raises exception when user exists."""
    email = 'test@mail.com'
    password = 'medtagger'
    first_name = 'First'
    last_name = 'Last'

    with pytest.raises(InvalidArgumentsException) as exception:
        create_user(email, password, first_name, last_name)
    assert str(exception.value) == 'User with this email already exist'


def test_create_user_missing_role(mocker: Any, get_user_by_email_failure_fixture: Any, get_role_fixture: Any) -> None:
    """Check if create user method raises exception when role does not exists."""
    email = 'test@mail.com'
    password = 'medtagger'
    first_name = 'First'
    last_name = 'Last'

    with pytest.raises(InvalidArgumentsException) as exception:
        create_user(email, password, first_name, last_name)
    assert str(exception.value) == 'Role does not exist.'


def test_sign_in_user_user_does_not_exists(mocker: Any, get_user_by_email_failure_fixture: Any) -> None:
    """Check if sign int method raises exception when user provides wrong password."""
    email = 'test@mail.com'
    password = 'medtagger'

    with pytest.raises(InvalidArgumentsException) as exception:
        sign_in_user(email, password)
    assert str(exception.value) == 'User does not exist.'


def test_sign_in_user_wrong_password(mocker: Any, get_user_by_email_success_fixture: Any,
                                     wrong_password_fixture: Any) -> None:
    """Check if sign int method raises exception when user provides wrong password."""
    email = 'test@mail.com'
    password = 'medtagger'

    with pytest.raises(InvalidArgumentsException) as exception:
        sign_in_user(email, password)
    assert str(exception.value) == 'Password does not match.'
