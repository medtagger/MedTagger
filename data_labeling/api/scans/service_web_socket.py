"""Module responsible for definition of Scans service available via WebSockets"""
import io
from typing import Dict
import dicom
from flask_socketio import Namespace, emit

from data_labeling.api import web_socket
from data_labeling.types import ScanID
from data_labeling.api.exceptions import InvalidArgumentsException
from data_labeling.api.scans.business import get_metadata, add_new_slice, get_slices_for_scan


class Slices(Namespace):
    """WebSocket handler for /slices namespace"""

    MAX_NUMBER_OF_SLICES_PER_REQUEST = 10

    def on_request_slices(self, request: Dict) -> None:
        """Handler for slices request"""
        assert request.get('scan_id'), 'ScanID is required!'
        scan_id = ScanID(str(request['scan_id']))
        begin = request.get('begin', 0)
        count = request.get('count', 1)

        scan_metadata = get_metadata(scan_id)
        number_of_slices = scan_metadata.get('number_of_slices', 0)
        smaller_than_zero = (begin < 0 or count < 0)
        out_of_range = (begin > number_of_slices or begin + count > number_of_slices)
        if smaller_than_zero or out_of_range:
            raise InvalidArgumentsException('Indices out of bound.')

        # Make sure that nobody will fetch whole scan at once. It could freeze our API.
        if count > self.MAX_NUMBER_OF_SLICES_PER_REQUEST:
            message = 'Cannot return more than {} slices per request.'.format(self.MAX_NUMBER_OF_SLICES_PER_REQUEST)
            raise InvalidArgumentsException(message)

        for index, image in enumerate(get_slices_for_scan(scan_id, begin, count)):
            emit('slice', {'scan_id': scan_id, 'index': begin + index, 'image': image})

    @staticmethod
    def on_upload_slice(request: Dict) -> None:
        """Handler for uploading new slices"""
        assert request.get('scan_id'), 'ScanID is required!'
        assert request.get('image'), 'Image is required!'
        scan_id = ScanID(str(request['scan_id']))
        image = request['image']

        image_bytes = io.BytesIO(image)
        dicom_image_file = dicom.read_file(image_bytes, force=True)
        add_new_slice(scan_id, dicom_image_file)
        emit('ack')


# Register above namespace
web_socket.on_namespace(Slices('/slices'))
