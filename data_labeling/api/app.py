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

from data_labeling.api import blueprint
from data_labeling.config import ConfigurationFile

# Import all services
from data_labeling.api.core.service import core_ns  # noqa
from data_labeling.api.scans.service import scans_ns  # noqa


# Load configuration
configuration = ConfigurationFile()

# Definition of application
app = Flask(__name__)
app.secret_key = configuration.get('api', 'secret_key', fallback='')
app.register_blueprint(blueprint)

# Application config
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'

if __name__ == '__main__':
    # Run the application
    host = configuration.get('api', 'host', fallback='localhost')
    port = configuration.getint('api', 'port', fallback=51000)
    debug = configuration.getboolean('api', 'debug', fallback=True)
    app.run(host=host, port=port, debug=debug)
