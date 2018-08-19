"""Module responsible for definition of Scans service available via WebSockets."""
from typing import Dict

from flask_socketio import Namespace, emit

from medtagger.api import web_socket
from medtagger.database.models import SliceOrientation
from medtagger.types import ScanID
from medtagger.api.exceptions import InvalidArgumentsException
from medtagger.api.scans import business


class Slices(Namespace):
    """WebSocket handler for /slices namespace."""

    MAX_NUMBER_OF_SLICES_PER_REQUEST = 25

    def on_request_slices(self, request: Dict) -> None:
        """Handle slices request triggered  by `request_slices` event."""
        assert request.get('scan_id'), 'ScanID is required!'
        scan_id = ScanID(str(request['scan_id']))
        begin = max(0, request.get('begin', 0))
        count = request.get('count', 1)
        reversed_order = request.get('reversed', False)
        orientation = request.get('orientation', SliceOrientation.Z.value)
        self._raise_on_invalid_request_slices(count, orientation)

        orientation = SliceOrientation[orientation]
        slices = list(business.get_slices_for_scan(scan_id, begin, count, orientation=orientation))
        slices_to_send = list(reversed(slices)) if reversed_order else slices
        last_in_batch = begin if reversed_order else begin + len(slices_to_send) - 1
        for index, (_slice, image) in enumerate(slices_to_send):
            emit('slice', {
                'scan_id': scan_id,
                'index': begin + index,
                'last_in_batch': last_in_batch,
                'image': image,
            })

    def _raise_on_invalid_request_slices(self, count: int, orientation: str) -> None:
        """Validate incoming request and raise an exception if there are issues with given arguments.

        :param count: number of slices that should be returned
        :param orientation: Slice's orientation as a string
        """
        # Make sure that passed orientation is proper one
        if orientation not in SliceOrientation.__members__:
            raise InvalidArgumentsException('Invalid Slice orientation.')

        # Make sure that nobody will fetch whole scan at once. It could freeze our backend application.
        if count > self.MAX_NUMBER_OF_SLICES_PER_REQUEST:
            message = 'Cannot return more than {} slices per request.'.format(self.MAX_NUMBER_OF_SLICES_PER_REQUEST)
            raise InvalidArgumentsException(message)


# Register above namespace
web_socket.on_namespace(Slices('/slices'))
