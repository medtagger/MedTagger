"""Module responsible for definition of Scans service available via WebSockets."""
from typing import Dict

from flask_socketio import Namespace, emit

from medtagger.api import web_socket
from medtagger.database.models import SliceOrientation
from medtagger.types import ScanID
from medtagger.api.exceptions import InvalidArgumentsException
from medtagger.api.scans import business
from medtagger.repositories import tasks as TasksRepository


class Slices(Namespace):
    """WebSocket handler for /slices namespace."""

    MAX_NUMBER_OF_SLICES_PER_REQUEST = 25

    def on_request_slices(self, request: Dict) -> None:
        """Handle slices request triggered  by `request_slices` event."""
        assert request.get('scan_id'), 'ScanID is required!'
        assert request.get('task_key'), 'Task Key is required!'

        scan_id = ScanID(str(request['scan_id']))
        task_key = request['task_key']
        begin = max(0, request.get('begin', 0))
        count = request.get('count', 1)
        reversed_order = request.get('reversed', False)
        request_orientation = request.get('orientation', SliceOrientation.Z.value)
        self._raise_on_invalid_request_slices(count, request_orientation)

        orientation = SliceOrientation[request_orientation]
        self._send_slices(scan_id, begin, count, orientation, reversed_order)
        if orientation == SliceOrientation.Z:
            self._send_predefined_labels(scan_id, begin, count, task_key, reversed_order)

    @staticmethod
    def _send_slices(scan_id: ScanID, begin: int, count: int, orientation: SliceOrientation,
                     reversed_order: bool = False) -> None:
        """Send Slices to the User using WebSocket.

        :param scan_id: ID of a Scan
        :param begin: first Slice index to be sent
        :param count: number of Slices to be sent
        :param orientation: orientation of Slices for this Scan
        :param reversed_order: (optional) emit Slices in reversed order
        """
        slices = list(business.get_slices_for_scan(scan_id, begin, count, orientation=orientation))
        slices_to_send = reversed(list(enumerate(slices))) if reversed_order else enumerate(slices)
        last_in_batch = begin if reversed_order else begin + len(slices) - 1
        for index, (_slice, image) in slices_to_send:
            emit('slice', {
                'scan_id': scan_id,
                'index': begin + index,
                'last_in_batch': last_in_batch,
                'image': image,
            })

    @staticmethod
    def _send_predefined_labels(scan_id: ScanID, begin: int, count: int, task_key: str,
                                reversed_order: bool = False) -> None:
        """Send Predefined Labels to the User using WebSocket.

        :param scan_id: ID of a Scan
        :param begin: first Slice index to be sent
        :param count: number of Slices to be sent
        :param task_key: key of a Task for which Predefined Labels should be sent
        :param reversed_order: (optional) emit Label Elements in reversed order
        """
        task = TasksRepository.get_task_by_key(task_key)
        label_elements = list(business.get_predefined_brush_label_elements(scan_id, task.id, begin, count))
        label_elements_to_send = reversed(list(label_elements)) if reversed_order else label_elements
        for label_element, image in label_elements_to_send:
            emit('brush_labels', {
                'scan_id': scan_id,
                'tag_key': label_element.tag.key,
                'index': label_element.slice_index,
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
