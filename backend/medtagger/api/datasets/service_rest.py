"""Module responsible for definition of Datasets service available via HTTP REST API."""
from typing import Any

from flask import request
from flask_restplus import Resource

from medtagger.api import api
from medtagger.api.datasets import serializers, business
from medtagger.api.security import login_required, role_required

datasets_ns = api.namespace('datasets', 'Methods related with datasets')


@datasets_ns.route('')
class Datasets(Resource):
    """Endpoint that manages datasets."""

    @staticmethod
    @login_required
    @datasets_ns.marshal_with(serializers.out__dataset)
    @datasets_ns.doc(security='token')
    @datasets_ns.doc(description='Returns all available Datasets.')
    @datasets_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Return all available datasets."""
        return business.get_available_datasets()

    @staticmethod
    @login_required
    @role_required('doctor', 'admin')
    @datasets_ns.expect(serializers.in__dataset)
    @datasets_ns.marshal_with(serializers.out__dataset)
    @datasets_ns.doc(security='token')
    @datasets_ns.doc(description='Create new Dataset.')
    @datasets_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create Dataset."""
        payload = request.json
        key = payload['key']
        name = payload['name']

        return business.create_dataset(key, name), 201
