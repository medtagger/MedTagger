"""Unit tests for data_labeling/config.py."""
from medtagger.config import AppConfiguration


def test_get_default_values_for_api() -> None:
    """Check if default values saved in unit test configuration is properly defined."""
    config = AppConfiguration()

    assert config.get('api', 'host') == 'localhost'
    assert config.getint('api', 'port') == 51000
    assert not config.getboolean('api', 'debug')
    assert config.get('api', 'secret_key') == 'SECRET_KEY'
    assert config.get('db', 'database_uri') == 'sqlite:///:memory:'
