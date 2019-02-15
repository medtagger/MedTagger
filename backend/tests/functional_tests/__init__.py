"""Module for global methods that may be useful during application testing."""
import functools
from typing import Any, Callable, Mapping
from gevent import monkey
monkey.patch_all()

# Put all MedTagger imports **after** gevent monkey patching
from medtagger import config  # noqa  # pylint: disable=wrong-import-position
from medtagger.storage import Storage  # noqa  # pylint: disable=wrong-import-position


def get_api_client() -> Any:
    """Return API client for testing purpose."""
    from medtagger.api.rest import app
    app.testing = True
    return app.test_client()


def get_web_socket_client(namespace: str = None) -> Any:
    """Return Web Socket client for testing purpose."""
    from medtagger.api.websocket import app, web_socket
    app.testing = True
    return web_socket.test_client(app, namespace=namespace)


def get_storage(mocker: Any, storage_backend_configuration: str) -> Storage:
    """Return Storage with a given backend that can be used for testing purpose."""
    def mocked_app_configuration_get(storage_backend_configuration: str, get_method: Callable[[str, str, Any], str],
                                     namespace: str, entry: str, fallback: Any = None) -> str:
        """Wrap `get` method for Application Configuration and follow up to original implementation if needed."""
        if namespace == 'storage' and entry == 'backend':
            return storage_backend_configuration
        return get_method(namespace, entry, fallback)

    # Mock configuration by wrapping `get` method with above function and return Storage object at the end
    configuration = config.AppConfiguration()
    mocked_storage_backend = functools.partial(mocked_app_configuration_get,
                                               storage_backend_configuration, configuration.get)
    mocker.patch.object(config.AppConfiguration, 'get', wraps=mocked_storage_backend)
    return Storage()


init_storage = get_storage  # An alias that will be more readable if someone would like only to initialize mock


def get_headers(**kwargs: Any) -> Mapping:
    """Return headers based on given key-value arguments."""
    headers = {}
    if kwargs.get('json'):
        headers['Content-Type'] = 'application/json'
    if kwargs.get('multipart'):
        headers['Content-Type'] = 'multipart/form-data'
    if kwargs.get('token'):
        headers['Authorization'] = 'Bearer ' + kwargs.get('token', '')
    return headers
