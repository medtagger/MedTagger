"""Module for global methods that may be useful during application testing."""
from typing import Any

import happybase
from flask.testing import FlaskClient


def get_test_application(mocker: Any) -> FlaskClient:
    """Return Flask application for unit testing.

    :param mocker: mocker object from PyTest
    :return: application for testing purpose
    """
    # IMPORTANT: Mock HBase ConnectionPool BEFORE(!) importing Flask application
    mocker.patch.object(happybase, 'ConnectionPool')

    from data_labeling.api.app import app

    app.testing = True
    return app.test_client()
