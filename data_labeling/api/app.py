"""Module responsible for definition of whole application

It is also a great entry point for running this app. To do so, you can use:

    $ python data_labeling/api/app.py
     * Running on http://localhost:51000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: XXX-XXX-XXX
"""
# pylint: disable=unused-import;  It's used by Flask
from flask import Flask
from flask_user import SQLAlchemyAdapter, UserMixin

from data_labeling.api import blueprint
from data_labeling.api.database import db

from data_labeling.api.database.models import User
from data_labeling.api.user.business import user_manager
from data_labeling.config import ConfigurationFile

# Import all services
from data_labeling.api.core.service import core_ns  # noqa
from data_labeling.api.scans.service import scans_ns  # noqa
from data_labeling.api.user.service import user_ns  # noqa

# Load configuration
configuration = ConfigurationFile()

# Definition of application
app = Flask(__name__)
app.secret_key = configuration.get('api', 'secret_key')
app.register_blueprint(blueprint)

# Application config
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['SQLALCHEMY_DATABASE_URI'] = configuration.get('db', 'database_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['USER_ENABLE_EMAIL'] = False
app.config['RESTPLUS_VALIDATE'] = True



db_adapter = SQLAlchemyAdapter(db, User)
user_manager.db_adapter = db_adapter
user_manager.init_app(app)

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    # Run the application
    host = configuration.get('api', 'host', fallback='localhost')
    port = configuration.getint('api', 'port', fallback=51000)
    debug = configuration.getboolean('api', 'debug', fallback=True)
    app.run(host=host, port=port, debug=debug, use_reloader=False)
