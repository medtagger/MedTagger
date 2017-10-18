"""Module responsible for business logic in all Scans endpoints"""
from random import randint, choice
from typing import Iterable, Dict, Any

from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.types import ScanID, LabelID, CuboidLabelPosition, CuboidLabelShape
from data_labeling.models.scan import Scan


def create_empty_scan() -> ScanID:
    """Create new empty scan

    :return: ID of a newly created scan
    """
    scan = Scan()
    scan.create_if_needed()
    return scan.id


def get_metadata(scan_id: ScanID) -> Dict[str, Any]:
    """Fetch metadata for given scan

    :param scan_id: ID of a given scan
    :return: dictionary with scan's metadata
    """
    scan = Scan(scan_id)
    number_of_slices = len(scan.slices_keys)

    return {
        'number_of_slices': number_of_slices,
    }


def get_random_scan() -> Dict[str, Any]:
    """Fetch random scan for labeling

    WARNING: Temporary implementation!
             This method may be highly inefficient as it queries HBase for all keys from Scans table!

    :return: dictionary with details about scan
    """
    hbase_client = HBaseClient()
    all_scans_keys = hbase_client.get_all_keys(HBaseClient.SCANS)
    scan_id = ScanID(choice(list(all_scans_keys)))
    scan = Scan(scan_id)
    number_of_slices = len(scan.slices_keys)

    return {
        'scan_id': scan_id,
        'number_of_slices': number_of_slices,
    }


def get_slices_for_scan(scan_id: ScanID, begin: int, count: int) -> Iterable[bytes]:
    """Fetch multiple slices for given scan

    WARNING: This will be replaced with query to HBase (once we will have converted data)!

    :param scan_id: ID of a given scan
    :param begin: first slice index (included)
    :param count: number of slices that will be returned
    :return: list of slices (each encoded in base64)
    """
    scan = Scan(scan_id)
    sorted_slices = sorted(list(scan.slices), key=lambda _slice: _slice.location)
    for _slice in sorted_slices[begin:begin + count]:
        yield _slice.converted_image


def add_cuboid_label(scan_id: ScanID, position: CuboidLabelPosition, shape: CuboidLabelShape) -> LabelID:
    """Add cuboid label to given scan

    :param scan_id: ID of a given scan
    :param position: position (upper top left vertex) of cuboid label within range 0..1
    :param shape: shape of cuboid label within range 0..1
    """
    # pylint: disable=unused-argument
    return LabelID(randint(0, 10000))


def add_new_slice(scan_id: ScanID, dicom_image_file: Any) -> None:
    """Add new slice for given Scan

    :param scan_id: ID of a Scan for which it should add new slice
    :param dicom_image_file: Dicom file with a single slice
    """
    scan = Scan(scan_id)
    scan.add_slice(dicom_image_file)
