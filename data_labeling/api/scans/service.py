"""Module responsible for definition of Scans service"""
from typing import Any
from flask import request
from flask_restplus import Resource

from data_labeling.types import ScanID, RectangleLabelPosition, RectangleLabelShape
from data_labeling.api import api
from data_labeling.api.scans import serializers
from data_labeling.api.scans.business import get_metadata, get_random_scan, get_slices_for_scan, add_rectangle_label
from data_labeling.api.exceptions import InvalidArgumentsException

scans_ns = api.namespace('scan', 'Methods related with scans')


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


@scans_ns.route('/slices')
class Slices(Resource):
    """Endpoint that returns slices from given scan"""

    MAX_NUMBER_OF_SLICES = 10

    @scans_ns.expect(serializers.slices_arguments, validate=True)
    @scans_ns.doc(description='Returns slices for given scan.')
    @scans_ns.doc(responses={200: 'Success', 400: 'Invalid arguments', 404: 'Could not find scan'})
    def get(self) -> Any:
        """Method responsible for returning scans from given scans"""
        args = serializers.slices_arguments.parse_args(request)
        scan_id = args['scan_id']
        begin = args['begin']
        end = args['end']

        # Check if people won't ask for something that cannot be fetched
        metadata = get_metadata(scan_id)
        if begin < 0 or end < 0 or begin > metadata['number_of_slices'] or end > metadata['number_of_slices']:
            raise InvalidArgumentsException('Indices out of bound.')

        # In case of invalid slices window response error with 400 code
        if begin > end:
            raise InvalidArgumentsException('End should be greater than or equal to begin.')

        # Make sure that nobody will fetch whole scan at once. It could freeze our API.
        if end - begin > self.MAX_NUMBER_OF_SLICES:
            message = 'Cannot return more than {} slices per request.'.format(self.MAX_NUMBER_OF_SLICES)
            raise InvalidArgumentsException(message)

        return get_slices_for_scan(scan_id, begin, end)


@scans_ns.route('/label/rectangle')
class LabelRectangle(Resource):
    """Endpoint that saves rectangle label for given scan"""

    @staticmethod
    @scans_ns.expect(serializers.rectangle_label, validate=True)
    @scans_ns.doc(description='Saves rectangle label and assigns it to given scan.')
    @scans_ns.doc(responses={200: 'Success', 400: 'Invalid arguments', 404: 'Could not find scan'})
    def post() -> Any:
        """Method responsible for saving new label for given scan"""
        payload = request.json

        scan_id = ScanID(payload['scan_id'])
        position = RectangleLabelPosition(x=payload['x'], y=payload['y'], z=payload['z'])
        shape = RectangleLabelShape(width=payload['width'], height=payload['height'], depth=payload['depth'])
        add_rectangle_label(scan_id, position, shape)

        return {'success': True}
