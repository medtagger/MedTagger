"""Module responsible for business logic in all Scans endpoints"""
import base64

from typing import List, Dict, Any

from data_labeling.types import ScanID


def get_metadata(scan_id: ScanID) -> Dict[str, Any]:  # pylint: disable=unused-argument
    """Fetch metadata for given scan

    WARNING: This will be replaced with database model (in the near future)!

    :param scan_id: ID of a given scan
    :return: dictionary with scan's metadata
    """
    return {
        'number_of_slices': 20,
    }


def get_slices_for_scan(scan_id: ScanID, begin: int, end: int) -> List[str]:  # pylint: disable=unused-argument
    """Fetch multiple slices for given scan

    WARNING: This will be replaced with query to HDFS (in the near future)!

    :param scan_id: ID of a given scan
    :param begin: first slice index (included)
    :param end: last slice index (excluded)
    :return: list of slices (each encoded in base64)
    """
    encoded_images = []
    for _ in range(begin, end):
        with open('example_data/example_slice.jpg', 'rb') as raw_data:
            encoded_image = base64.b64encode(raw_data.read()).decode('utf-8')
            encoded_images.append(encoded_image)
    return encoded_images
