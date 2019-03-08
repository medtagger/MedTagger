"""Module responsible for definition of WebSocket application.

It is also a great entry point for running WebSocket's endpoints. To do so, you can use:

    $ python medtagger/api/websocket.py

"""  # pylint: disable=duplicate-code;  This is one of two application entrypoints
# pylint: disable=unused-import;  It's used by Flask
# pylint: disable=wrong-import-position;  Python logging should be configured ASAP
import logging.config
from typing import Any
from gevent import monkey
monkey.patch_all()

# Setup logging as fast as possible, so imported libraries __init__.py will
# be able to log using our configuration of logging
logging.config.fileConfig('logging.conf')
from flask import Flask  # noqa
from flask_cors import CORS  # noqa

from medtagger.api import web_socket, setup_connection_to_sql_and_storage  # noqa
from medtagger.config import AppConfiguration  # noqa
from medtagger.database import Session  # noqa

# Import all WebSocket services
from medtagger.api.scans.service_web_socket import Slices as slices_websocket_ns  # noqa

logger = logging.getLogger(__name__)

# Load configuration
logger.info('Loading configuration file...')
configuration = AppConfiguration()
host = configuration.get('api', 'host', fallback='localhost')
port = configuration.getint('api', 'websocket_port', fallback=51001)
debug = configuration.getboolean('api', 'debug', fallback=True)

# Definition of application
app = Flask(__name__)
CORS(app)
app.secret_key = configuration.get('api', 'secret_key', fallback='')
web_socket.init_app(app)
setup_connection_to_sql_and_storage()


@app.teardown_appcontext
def shutdown_session(exception: Any = None) -> None:  # pylint: disable=unused-argument
    """Remove Session on each Request end."""
    Session.remove()


if __name__ == '__main__':
    web_socket.run(app, host=host, port=port, debug=debug)
