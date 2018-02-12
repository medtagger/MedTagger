"""Module responsible for definition of whole application.

It is also a great entry point for running this app. To do so, you can use:

    $ python medtagger/api/app.py
     * Running on http://localhost:51000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: XXX-XXX-XXX
"""
# pylint: disable=unused-import;  It's used by Flask
# pylint: disable=wrong-import-position;  Python logging should be configured ASAP
import logging.config

# Setup logging as fast as possible, so imported libraries __init__.py will
# be able to log using our configuration of logging
logging.config.fileConfig('logging.conf')
from flask import Flask, current_app  # noqa
from flask_cors import CORS  # noqa
from flask_security import Security, SQLAlchemyUserDatastore  # noqa

from medtagger.api import blueprint, web_socket  # noqa
from medtagger.config import AppConfiguration  # noqa
from medtagger.database import db  # noqa
from medtagger.database.models import User, Role  # noqa

# Import all REST services
from medtagger.api.core.service import core_ns as core_rest_ns  # noqa
from medtagger.api.labels.service import labels_ns  # noqa
from medtagger.api.scans.service_rest import scans_ns as scans_rest_ns  # noqa
from medtagger.api.users.service import users_ns  # noqa
from medtagger.api.auth.service import auth_ns  # noqa

# Import all WebSocket services
from medtagger.api.scans.service_web_socket import Slices as slices_websocket_ns  # noqa

logger = logging.getLogger(__name__)

# Load configuration
logger.info('Loading configuration file...')
configuration = AppConfiguration()

# Definition of application
app = Flask(__name__)
CORS(app)
app.secret_key = configuration.get('api', 'secret_key', fallback='')
app.register_blueprint(blueprint)
web_socket.init_app(app)

# Application config
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['SQLALCHEMY_DATABASE_URI'] = configuration.get('db', 'database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['RESTPLUS_VALIDATE'] = True

# Prepare adapter for user management
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
security.init_app(app, user_datastore)

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        current_app.login_manager.login_view = None

    # Run the application
    host = configuration.get('api', 'host', fallback='localhost')
    port = configuration.getint('api', 'port', fallback=51000)
    debug = configuration.getboolean('api', 'debug', fallback=True)
    web_socket.run(app, host=host, port=port, debug=debug)
