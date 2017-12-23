"""Module responsible for definition of whole application.

It is also a great entry point for running this app. To do so, you can use:

    $ python medtagger/api/app.py
     * Running on http://localhost:51000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: XXX-XXX-XXX
"""
# pylint: disable=unused-import;  It's used by Flask
from flask import Flask, current_app
from flask_cors import CORS

from medtagger.api import blueprint, web_socket
from medtagger.api.account.business import security, user_datastore
from medtagger.database import db
from medtagger.config import AppConfiguration

# Import all REST services
from medtagger.api.core.service import core_ns as core_rest_ns  # noqa
from medtagger.api.labels.service import labels_ns  # noqa
from medtagger.api.scans.service_rest import scans_ns as scans_rest_ns  # noqa
from medtagger.api.account.service import account_ns  # noqa
from medtagger.api.users.service import users_ns  # noqa

# Import all WebSocket services
from medtagger.api.scans.service_web_socket import Slices as slices_websocket_ns  # noqa


# Load configuration
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
