"""Module responsible for defining API"""
import logging
import traceback
from typing import Tuple, Dict

from flask import Blueprint
from flask_restplus import Api
from flask_socketio import SocketIO, emit

from data_labeling.api.exceptions import InvalidArgumentsException, BusinessLogicException

log = logging.getLogger(__name__)

# Definition of the API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='0.1', title='Backend API', description='Documentation for Backend API', validate=True)
web_socket = SocketIO(logger=True, engineio_logger=True)


@api.errorhandler
def rest_default_error_handler(exception: Exception) -> Tuple[Dict, int]:  # pylint: disable=unused-argument
    """Handler for all unhandled exceptions

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    log.error(traceback.format_exc())
    return {'message': 'An unhandled exception occurred.'}, 500


@api.errorhandler(BusinessLogicException)
def rest_business_logic_error_handler(exception: Exception) -> Tuple[Dict, int]:
    """Handler for business logic errors

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    log.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'Business logic error.', 'details': details}, 500


@api.errorhandler(InvalidArgumentsException)
def rest_invalid_arguments_error_handler(exception: Exception) -> Tuple[Dict, int]:
    """Handler for invalid arguments errors

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    log.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'Invalid arguments.', 'details': details}, 400


@web_socket.on_error_default
def web_socket_default_error_handler(exception: Exception) -> None:  # pylint: disable=unused-argument
    """Handler for all unhandled exceptions

    :param exception: Python Exception
    """
    log.error(traceback.format_exc())
    emit('error', {'message': 'An unhandled exception occurred.'})
