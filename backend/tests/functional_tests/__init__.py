"""Module for global methods that may be useful during application testing."""
from typing import Mapping, Any
from gevent import monkey
monkey.patch_all()


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
