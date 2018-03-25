"""Module for global methods that may be useful during application testing."""
from typing import Any


def get_api_client() -> Any:
    """Get API client for testing purpose."""
    from medtagger.api.rest import app
    app.testing = True
    return app.test_client()


def get_web_socket_client(namespace: str = None) -> Any:
    """Get Web Socket client for testing purpose."""
    from medtagger.api.websocket import app, web_socket
    app.testing = True
    return web_socket.test_client(app, namespace=namespace)
