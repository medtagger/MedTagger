"""Module responsible for definition of Scans service available via WebSockets"""
from typing import Dict

from flask_socketio import Namespace, emit

from data_labeling.api import web_socket
from data_labeling.types import ScanID
from data_labeling.api.exceptions import InvalidArgumentsException
from data_labeling.api.scans import business


class Slices(Namespace):
    """WebSocket handler for /slices namespace"""

    MAX_NUMBER_OF_SLICES_PER_REQUEST = 10

    def on_request_slices(self, request: Dict) -> None:
        """Handler for slices request triggered  by `request_slices` event"""
        assert request.get('scan_id'), 'ScanID is required!'
        scan_id = ScanID(str(request['scan_id']))
        begin = request.get('begin', 0)
        count = request.get('count', 1)
        self._raise_on_invalid_request_slices(scan_id, begin, count)

        for index, (_slice, image) in enumerate(business.get_slices_for_scan(scan_id, begin, count)):
            emit('slice', {'scan_id': scan_id, 'index': begin + index, 'image': image})

    @staticmethod
    def on_upload_slice(request: Dict) -> None:
        """Handler for uploading new slices triggered by `upload_slice` event"""
        assert request.get('scan_id'), 'ScanID is required!'
        assert request.get('image'), 'Image is required!'
        scan_id = ScanID(str(request['scan_id']))
        image = request['image']

        business.add_new_slice(scan_id, image)
        emit('ack', {'success': True})

    def _raise_on_invalid_request_slices(self, scan_id: ScanID, begin: int, count: int) -> None:
        """Validate incoming request and raise an exception if there are issues with given arguments

        :param scan_id: ID of a Scan
        :param begin: beginning of the requested window
        :param count: number of slices that should be returned
        """
        scan_metadata = business.get_metadata(scan_id)
        number_of_slices = scan_metadata.number_of_slices
        smaller_than_zero = (begin < 0 or count < 0)
        out_of_range = (begin > number_of_slices or begin + count > number_of_slices)
        if smaller_than_zero or out_of_range:
            raise InvalidArgumentsException('Indices out of bound.')

        # Make sure that nobody will fetch whole scan at once. It could freeze our backend application.
        if count > self.MAX_NUMBER_OF_SLICES_PER_REQUEST:
            message = 'Cannot return more than {} slices per request.'.format(self.MAX_NUMBER_OF_SLICES_PER_REQUEST)
            raise InvalidArgumentsException(message)


# Register above namespace
web_socket.on_namespace(Slices('/slices'))
