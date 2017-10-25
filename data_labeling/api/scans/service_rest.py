"""Module responsible for definition of Scans service available via HTTP REST API"""
from typing import Any
from flask import request
from flask_restplus import Resource

from data_labeling.types import ScanID, CuboidLabelPosition, CuboidLabelShape
from data_labeling.api import api
from data_labeling.api.scans import serializers
from data_labeling.api.scans.business import create_empty_scan, get_random_scan, add_cuboid_label

scans_ns = api.namespace('scans', 'Methods related with scans')


@scans_ns.route('/')
class Scans(Resource):
    """Endpoint that can create new scan"""

    @staticmethod
    @scans_ns.marshal_with(serializers.new_scan)
    @scans_ns.doc(description='Creates empty scan.')
    @scans_ns.doc(responses={201: 'Success'})
    def post() -> Any:
        """Method responsible for creating empty scan"""
        scan_id = create_empty_scan()
        return {'scan_id': scan_id}, 201


@scans_ns.route('/random')
class Random(Resource):
    """Endpoint that returns random scan for labeling"""

    @staticmethod
    @scans_ns.marshal_with(serializers.random_scan)
    @scans_ns.doc(description='Returns random scan.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Method responsible for returning random scan's metadata"""
        return get_random_scan()


@scans_ns.route('/<string:scan_id>/label/cuboid')
@scans_ns.param('scan_id', 'Scan identifier')
class LabelCuboid(Resource):
    """Endpoint that saves cuboid label for given scan"""

    @staticmethod
    @scans_ns.expect(serializers.cuboid_label, validate=True)
    @scans_ns.doc(description='Saves cuboid label and assigns it to given scan.')
    @scans_ns.doc(responses={201: 'Successfully saved', 400: 'Invalid arguments', 404: 'Could not find scan'})
    def post(scan_id: ScanID) -> Any:
        """Method responsible for saving new cuboid label for given scan"""
        payload = request.json

        position = CuboidLabelPosition(x=payload['x'], y=payload['y'], z=payload['z'])
        shape = CuboidLabelShape(width=payload['width'], height=payload['height'], depth=payload['depth'])
        label_id = add_cuboid_label(scan_id, position, shape)

        return {'label_id': label_id}, 201
