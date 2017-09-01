"""Module responsible for business logic in all Scans endpoints"""
import base64
from random import randint

from typing import List, Dict, Any

from data_labeling.types import ScanID, LabelID, CuboidLabelPosition, CuboidLabelShape


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
    scan_id = ScanID(randint(0, 10000))
    metadata = get_metadata(scan_id)
    begin = randint(0, 10)
    count = randint(0, 10)

    return {
        'scan_id': scan_id,
        'slices_begin': begin,
        'slices_count': count,
        'total_number_of_slices': metadata.get('number_of_slices'),
    }


def get_slices_for_scan(scan_id: ScanID, begin: int, count: int) -> List[str]:
    """Fetch multiple slices for given scan

    WARNING: This will be replaced with query to HDFS (in the near future)!

    :param scan_id: ID of a given scan
    :param begin: first slice index (included)
    :param count: number of slices that will be returned
    :return: list of slices (each encoded in base64)
    """
    # pylint: disable=unused-argument
    with open('example_data/example_slice.jpg', 'rb') as raw_data:
        encoded_image = base64.b64encode(raw_data.read()).decode('utf-8')
    encoded_images = [encoded_image] * count
    return encoded_images


def add_cuboid_label(scan_id: ScanID, position: CuboidLabelPosition, shape: CuboidLabelShape) -> LabelID:
    """Add cuboid label to given scan

    :param scan_id: ID of a given scan
    :param position: position (upper top left vertex) of cuboid label within range 0..1
    :param shape: shape of cuboid label within range 0..1
    """
    # pylint: disable=unused-argument
    return LabelID(randint(0, 10000))
