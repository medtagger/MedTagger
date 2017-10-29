"""Module responsible for business logic in all Scans endpoints"""
from typing import Iterable, Dict, Any

from retrying import retry
from dicom.dataset import FileDataset
from sqlalchemy.sql.expression import func

from data_labeling.api.exceptions import NotFoundException
from data_labeling.types import ScanID, LabelID, CuboidLabelPosition, CuboidLabelShape
from data_labeling.database import db_session
from data_labeling.database.models import Scan


def create_empty_scan() -> ScanID:
    """Create new empty scan

    :return: ID of a newly created scan
    """
    with db_session() as session:
        scan = Scan()
        session.add(scan)
    return scan.id


def get_metadata(scan_id: ScanID) -> Dict[str, Any]:
    """Fetch metadata for given scan

    :param scan_id: ID of a given scan
    :return: dictionary with scan's metadata
    """
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
    number_of_slices = len(scan.slices)

    return {
        'number_of_slices': number_of_slices,
    }


@retry(stop_max_attempt_number=5, retry_on_exception=lambda ex: isinstance(ex, NotFoundException))
def get_random_scan() -> Dict[str, Any]:
    """Fetch random scan for labeling

    :return: dictionary with details about scan
    """
    with db_session() as session:
        scan = session.query(Scan).order_by(func.random()).first()
    number_of_slices = len(scan.slices)
    if not number_of_slices:
        raise NotFoundException('Could not find any Scan that has at least one Slice!')

    return {
        'scan_id': scan.id,
        'number_of_slices': number_of_slices,
    }


def get_slices_for_scan(scan_id: ScanID, begin: int, count: int) -> Iterable[bytes]:
    """Fetch multiple slices for given scan

    :param scan_id: ID of a given scan
    :param begin: first slice index (included)
    :param count: number of slices that will be returned
    :return: list of slices (each encoded in base64)
    """
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
    for _slice in scan.slices[begin:begin + count]:
        yield _slice.converted_image


def add_cuboid_label(scan_id: ScanID, position: CuboidLabelPosition, shape: CuboidLabelShape) -> LabelID:
    """Add cuboid label to given scan

    :param scan_id: ID of a given scan
    :param position: position (upper top left vertex) of cuboid label within range 0..1
    :param shape: shape of cuboid label within range 0..1
    """
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
        label_id = scan.add_label(position, shape)
    return label_id


def add_new_slice(scan_id: ScanID, dicom_image: FileDataset) -> None:
    """Add new slice for given Scan

    :param scan_id: ID of a Scan for which it should add new slice
    :param dicom_image: Dicom file with a single slice
    """
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
        scan.add_slice(dicom_image)
