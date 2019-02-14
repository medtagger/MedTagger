"""Module for global methods that may be useful during application testing."""
from typing import Any

from flask.testing import FlaskClient


def get_test_application(mocker: Any) -> FlaskClient:
    """Return Flask application for unit testing.

    :param mocker: mocker object from PyTest
    :return: application for testing purpose
    """
    # IMPORTANT: Mock Cassandra Connection BEFORE(!) importing Flask application
    mocker.patch('medtagger.storage.cassandra.CassandraStorageBackend._create_connection')

    from medtagger.api.rest import app

    app.testing = True
    return app.test_client()
