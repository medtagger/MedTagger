"""Module responsible for definition of Scans service available via HTTP REST API"""
from typing import Any
from flask import request
from flask_restplus import Resource

from data_labeling.types import ScanID
from data_labeling.api import api
from data_labeling.api.exceptions import InvalidArgumentsException
from data_labeling.api.scans import serializers
from data_labeling.api.scans.business import create_empty_scan, get_available_scan_categories, create_scan_category, \
    get_random_scan, add_label

scans_ns = api.namespace('scans', 'Methods related with scans')


@scans_ns.route('/')
class Scans(Resource):
    """Endpoint that can create new scan"""

    @staticmethod
    @scans_ns.expect(serializers.new_scan_request, validate=True)
    @scans_ns.marshal_with(serializers.new_scan_response)
    @scans_ns.doc(description='Creates empty scan.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Method responsible for creating empty scan"""
        payload = request.json
        category_key = payload.get('category', '')

        # Category validation cannot be done during request parsing, because Enums in serializers load on
        #  application boot-up
        if category_key not in [category.key for category in get_available_scan_categories()]:
            raise InvalidArgumentsException('Category "{}" is not available.'.format(category_key))

        scan_id = create_empty_scan(category_key)
        return {'scan_id': scan_id}, 201


@scans_ns.route('/categories')
class ScanCategories(Resource):
    """Endpoint that manages categories"""

    @staticmethod
    @scans_ns.marshal_with(serializers.scan_category)
    @scans_ns.doc(description='Returns all available scan categories.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Method responsible for returning all available scan categories"""
        return get_available_scan_categories()

    @staticmethod
    @scans_ns.expect(serializers.scan_category, validate=True)
    @scans_ns.marshal_with(serializers.scan_category)
    @scans_ns.doc(description='Returns all available scan categories.')
    @scans_ns.doc(responses={200: 'Success'})
    def post() -> Any:
        """Method responsible for creating empty scan"""
        payload = request.json
        key = payload.get('key', '')
        name = payload.get('name', '')
        image_path = payload.get('image_path', '')

        return create_scan_category(key, name, image_path)


@scans_ns.route('/random')
class Random(Resource):
    """Endpoint that returns random scan for labeling"""

    @staticmethod
    @scans_ns.expect(serializers.random_scan_arguments, validate=True)
    @scans_ns.marshal_with(serializers.random_scan)
    @scans_ns.doc(description='Returns random scan.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Method responsible for returning random scan's metadata"""
        args = serializers.random_scan_arguments.parse_args(request)
        category_key = args.category
        if category_key not in [category.key for category in get_available_scan_categories()]:
            raise InvalidArgumentsException('Category "{}" is not available.'.format(category_key))

        return get_random_scan(category_key)


@scans_ns.route('/<string:scan_id>/label')
@scans_ns.param('scan_id', 'Scan identifier')
class Label(Resource):
    """Endpoint that stores label for given scan"""

    @staticmethod
    @scans_ns.expect(serializers.label, validate=True)
    @scans_ns.doc(description='Stores label and assigns it to given scan.')
    @scans_ns.doc(responses={201: 'Successfully saved', 400: 'Invalid arguments', 404: 'Could not find scan'})
    def post(scan_id: ScanID) -> Any:
        """Method responsible for saving new label for given scan"""
        payload = request.json
        selections = payload.get('selections', [])
        label_id = add_label(scan_id, selections)

        return {'label_id': label_id}, 201
