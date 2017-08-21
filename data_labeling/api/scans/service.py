"""Module responsible for definition of Scans service"""
from typing import Any
from flask import request
from flask_restplus import Resource

from data_labeling.api import api
from data_labeling.api.scans import serializers
from data_labeling.api.scans.business import get_metadata, get_slices_for_scan
from data_labeling.api.exceptions import InvalidArgumentsException

scans_ns = api.namespace('scan', 'Methods related with scans')


@scans_ns.route('/metadata')
class Metadata(Resource):
    """Endpoint that returns metadata for given scan"""

    @staticmethod
    @scans_ns.expect(serializers.metadata_arguments, validate=True)
    @scans_ns.marshal_with(serializers.metadata)
    @scans_ns.doc(description='Returns metadata for given scan.')
    @scans_ns.doc(responses={200: 'Success'})
    def get() -> Any:
        """Method responsible for returning scan's metadata"""
        args = serializers.metadata_arguments.parse_args(request)
        scan_id = args['scan_id']

        return get_metadata(scan_id)


@scans_ns.route('/slices')
class Slices(Resource):
    """Endpoint that returns slices from given scan"""

    MAX_NUMBER_OF_SLICES = 10

    @scans_ns.expect(serializers.slices_arguments, validate=True)
    @scans_ns.doc(description='Returns slices for given scan.')
    @scans_ns.doc(responses={200: 'Success', 400: 'Invalid arguments'})
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
