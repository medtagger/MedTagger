"""Module responsible for definition of Scans service available via HTTP REST API."""
from typing import Any
from flask import request
from flask_restplus import Resource

from medtagger.types import ScanID
from medtagger.api import api
from medtagger.api.exceptions import InvalidArgumentsException
from medtagger.api.scans import business, serializers

scans_ns = api.namespace('scans', 'Methods related with scans')


@scans_ns.route('/')
class Scans(Resource):
    """Endpoint that can create new scan."""

    @staticmethod
    @scans_ns.expect(serializers.in__new_scan)
    @scans_ns.marshal_with(serializers.out__new_scan)
    @scans_ns.doc(description='Creates empty scan.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create empty scan."""
        payload = request.json
        category_key = payload['category']
        if not business.scan_category_is_valid(category_key):
            raise InvalidArgumentsException('Category "{}" is not available.'.format(category_key))

        scan = business.create_empty_scan(category_key)
        return scan, 201


@scans_ns.route('/categories')
class ScanCategories(Resource):
    """Endpoint that manages categories."""

    @staticmethod
    @scans_ns.marshal_with(serializers.inout__scan_category)
    @scans_ns.doc(description='Returns all available scan categories.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Return all available scan categories."""
        return business.get_available_scan_categories()

    @staticmethod
    @scans_ns.expect(serializers.inout__scan_category)
    @scans_ns.marshal_with(serializers.inout__scan_category)
    @scans_ns.doc(description='Returns all available scan categories.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Create empty scan."""
        payload = request.json
        key = payload['key']
        name = payload['name']
        image_path = payload['image_path']

        return business.create_scan_category(key, name, image_path), 201


@scans_ns.route('/random')
class Random(Resource):
    """Endpoint that returns random scan for labeling."""

    @staticmethod
    @scans_ns.expect(serializers.args__random_scan)
    @scans_ns.marshal_with(serializers.out__scan)
    @scans_ns.doc(description='Returns random scan.')
    @scans_ns.doc(responses={200: 'Success', 400: 'Invalid arguments', 404: 'No Scans available'})
    def get() -> Any:
        """Return random scan's metadata."""
        args = serializers.args__random_scan.parse_args(request)
        category_key = args.category
        if not business.scan_category_is_valid(category_key):
            raise InvalidArgumentsException('Category "{}" is not available.'.format(category_key))

        return business.get_random_scan(category_key)._asdict()


@scans_ns.route('/<string:scan_id>/label')
@scans_ns.param('scan_id', 'Scan identifier')
class Label(Resource):
    """Endpoint that stores label for given scan."""

    @staticmethod
    @scans_ns.expect(serializers.in__label)
    @scans_ns.marshal_with(serializers.out__label)
    @scans_ns.doc(description='Stores label and assigns it to given scan.')
    @scans_ns.doc(responses={201: 'Successfully saved', 400: 'Invalid arguments', 404: 'Could not find scan'})
    def post(scan_id: ScanID) -> Any:
        """Save new label for given scan."""
        payload = request.json
        selections = payload['selections']

        label = business.add_label(scan_id, selections)
        return label, 201


@scans_ns.route('/<string:scan_id>')
@scans_ns.param('scan_id', 'Scan identifier')
class Scan(Resource):
    """Endpoint that returns scan for the given scan id."""

    @staticmethod
    @scans_ns.marshal_with(serializers.out__scan)
    @scans_ns.doc(description='Returns scan with given scan_id.')
    @scans_ns.doc(responses={200: 'Success', 404: 'Could not find scan'})
    def get(scan_id: ScanID) -> Any:
        """Return scan for the given scan_id."""
        return business.get_scan(scan_id)._asdict()
