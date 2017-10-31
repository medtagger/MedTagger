"""Module responsible for business logic in all Scans endpoints"""
from typing import Iterable, Dict, List, Any

from dicom.dataset import FileDataset
from sqlalchemy.sql.expression import func

from data_labeling.api.exceptions import NotFoundException
from data_labeling.types import ScanID, LabelID, LabelPosition, LabelShape
from data_labeling.database import db_session
from data_labeling.database.models import Scan, ScanCategory


def get_available_scan_categories() -> List[ScanCategory]:
    """Fetch list of all available Scan Categories

    :return: list of Scan Categories
    """
    with db_session() as session:
        categories = session.query(ScanCategory).order_by(ScanCategory.id).all()
    return categories


def create_scan_category(key: str, name: str, image_path: str) -> ScanCategory:
    """Create new Scan Category

    :param key: unique key representing Scan Category
    :param name: name which describes this Category
    :param image_path: path to the image which is located on the frontend
    :return: Scan Category object
    """
    with db_session() as session:
        category = ScanCategory(key, name, image_path)
        session.add(category)
    return category


def create_empty_scan(category_key: str) -> ScanID:
    """Create new empty scan

    :param category_key: string with category key
    :return: ID of a newly created scan
    """
    with db_session() as session:
        category = session.query(ScanCategory).filter(ScanCategory.key == category_key).one()
        scan = Scan(category)
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


def get_random_scan(category_key: str) -> Dict[str, Any]:
    """Fetch random scan for labeling

    :param category_key: unique key identifying category
    :return: dictionary with details about scan
    """
    with db_session() as session:
        query = session.query(Scan)
        query = query.join(ScanCategory)
        query = query.filter(ScanCategory.key == category_key)
        query = query.filter(Scan.slices.any())  # type: ignore  # Could not find `any()` method.
        query = query.order_by(func.random())
        scan = query.first()
    if not scan:
        raise NotFoundException('Could not find any Scan for this category!')

    return {
        'scan_id': scan.id,
        'number_of_slices': len(scan.slices),
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


def add_label(scan_id: ScanID, selections: List[Dict]) -> LabelID:
    """Add label to given scan

    :param scan_id: ID of a given scan
    :param selections: List of JSONs describing selections for a single label
    """
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
        label = scan.create_label()

        for selection in selections:
            position = LabelPosition(x=selection.get('x', 0.0), y=selection.get('y', 0.0),
                                     slice_index=selection.get('slice_index', 0.0))
            shape = LabelShape(width=selection.get('width', 0.0), height=selection.get('height', 0.0))
            label.add_selection(position, shape)

    return label.id


def add_new_slice(scan_id: ScanID, dicom_image: FileDataset) -> None:
    """Add new slice for given Scan

    :param scan_id: ID of a Scan for which it should add new slice
    :param dicom_image: Dicom file with a single slice
    """
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
        scan.add_slice(dicom_image)
