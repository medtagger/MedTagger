"""Module responsible for business logic in all Scans endpoints"""
import base64
from random import randint

from typing import List, Dict, Any

from data_labeling.types import ScanID, RectangleLabelPosition, RectangleLabelShape


def get_metadata(scan_id: ScanID) -> Dict[str, Any]:
    """Fetch metadata for given scan

    WARNING: This will be replaced with database model (in the near future)!

    :param scan_id: ID of a given scan
    :return: dictionary with scan's metadata
    """
    # pylint: disable=unused-argument
    return {
        'number_of_slices': 20,
    }


def get_random_scan() -> Dict[str, Any]:
    """Fetch random scan for labeling

    WARNING: This will be replaced with some fancier implementation (in the near future)!

    :return: dictionary with details about scan
    """
    scan_id = ScanID('scan-hash-123')
    metadata = get_metadata(scan_id)
    begin = randint(5, 15) - 5
    end = begin + 10

    return {
        'scan_id': scan_id,
        'slices_begin': begin,
        'slices_end': end,
        'total_number_of_slices': metadata.get('number_of_slices'),
    }


def get_slices_for_scan(scan_id: ScanID, begin: int, end: int) -> List[str]:
    """Fetch multiple slices for given scan

    WARNING: This will be replaced with query to HDFS (in the near future)!

    :param scan_id: ID of a given scan
    :param begin: first slice index (included)
    :param end: last slice index (excluded)
    :return: list of slices (each encoded in base64)
    """
    # pylint: disable=unused-argument
    encoded_images = []
    for _ in range(begin, end):
        with open('example_data/example_slice.jpg', 'rb') as raw_data:
            encoded_image = base64.b64encode(raw_data.read()).decode('utf-8')
            encoded_images.append(encoded_image)
    return encoded_images


def add_rectangle_label(scan_id: ScanID, position: RectangleLabelPosition, shape: RectangleLabelShape) -> None:
    """Add rectangle label to given scan

    :param scan_id: ID of a given scan
    :param position: position (upper top left vertex) of rectangle label within range 0..1
    :param shape: shape of rectangle label within range 0..1
    """
    # pylint: disable=unused-argument
    pass
