"""Module responsible for defining API."""
import logging
import traceback
from typing import Tuple, Dict

from flask import Blueprint
from flask_restplus import Api
from flask_socketio import SocketIO, emit

from medtagger.api.exceptions import UnauthorizedException, InvalidArgumentsException, NotFoundException, \
    BusinessLogicException, AccessForbiddenException

logger = logging.getLogger(__name__)

# Definition of the API
authorizations = {
    'token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    },
}
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='0.1', title='Backend API', description='Documentation for Backend API',
          authorizations=authorizations, validate=True)
web_socket = SocketIO(logger=True, engineio_logger=True)


@api.errorhandler
def rest_default_error_handler(exception: Exception) -> Tuple[Dict, int]:  # pylint: disable=unused-argument
    """Handle all unhandled exceptions.

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    logger.error(traceback.format_exc())
    return {'message': 'An unhandled exception occurred.'}, 500


@api.errorhandler(BusinessLogicException)
def rest_business_logic_error_handler(exception: Exception) -> Tuple[Dict, int]:
    """Handle business logic errors.

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    logger.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'Business logic error.', 'details': details}, 500


@api.errorhandler(UnauthorizedException)
def rest_unauthorized_error_handler(exception: Exception) -> Tuple[Dict, int]:
    """Handle unauthorized errors.

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    logger.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'You are not authorized to use this method.', 'details': details}, 401


@api.errorhandler(NotFoundException)
def rest_not_found_error_handler(exception: Exception) -> Tuple[Dict, int]:
    """Handle not found errors.

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    logger.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'Requested object does not exist.', 'details': details}, 404


@api.errorhandler(InvalidArgumentsException)
def rest_invalid_arguments_error_handler(exception: Exception) -> Tuple[Dict, int]:
    """Handle invalid arguments errors.

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    logger.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'Invalid arguments.', 'details': details}, 400


@api.errorhandler(AccessForbiddenException)
def rest_access_forbidden_error_handel(exception: Exception) -> Tuple[Dict, int]:
    """Handle access forbidden errors.

    :param exception: Python Exception
    :return: tuple with response and status code
    """
    logger.warning(traceback.format_exc())
    details = str(exception)
    return {'message': 'Access forbidden', 'details': details}, 403


@web_socket.on_error_default
def web_socket_default_error_handler(exception: Exception) -> None:  # pylint: disable=unused-argument
    """Handle all unhandled exceptions.

    :param exception: Python Exception
    """
    logger.exception('An unhandled exception occurred.')
    emit('error', {'message': 'An unhandled exception occurred.'})
