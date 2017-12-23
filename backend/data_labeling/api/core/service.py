"""Module responsible for definition of Core service."""
from typing import Any

from flask_security import login_required, roles_required
from flask_restplus import Resource

from data_labeling.api import api
from data_labeling.api.core import business, serializers

core_ns = api.namespace('core', 'Core methods')


@core_ns.route('/status')
class Status(Resource):
    """Status endpoint that checks if everything is all right."""

    @staticmethod
    @core_ns.marshal_with(serializers.out__status)
    @core_ns.doc(description='Checks if API is running properly.')
    @core_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Return status of the API."""
        return business.success()


@core_ns.route('/check-authentication')
class CheckAuthentication(Resource):
    """Endpoint gives the possibility to check authorization mechanism."""

    @staticmethod
    @login_required
    @api.doc(responses={204: "User authenticated", 401: "Unauthorized"})
    def get() -> Any:
        """Check if the user is authenticated."""
        return {}, 204


@core_ns.route('/check-authorization')
class CheckAuthorization(Resource):
    """Endpoint to check if user has properly set role."""

    @staticmethod
    @login_required
    @roles_required('volunteer')
    def get() -> Any:
        """Endpoint to check if user has properly set role."""
        return {}, 204
