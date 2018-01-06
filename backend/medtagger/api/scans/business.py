"""Module responsible for business logic in all Scans endpoints."""
from typing import Iterable, Dict, List, Tuple

from sqlalchemy.orm.exc import NoResultFound

from medtagger.api.exceptions import NotFoundException
from medtagger.types import ScanID, LabelPosition, LabelShape, LabelSelectionBinaryMask, ScanMetadata
from medtagger.database.models import ScanCategory, Scan, Slice, Label, SliceOrientation
from medtagger.repositories.labels import LabelsRepository
from medtagger.repositories.slices import SlicesRepository
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.scan_categories import ScanCategoriesRepository
from medtagger.workers.conversion import convert_scan_to_png
from medtagger.workers.storage import store_dicom


def get_available_scan_categories() -> List[ScanCategory]:
    """Fetch list of all available Scan Categories.

    :return: list of Scan Categories
    """
    return ScanCategoriesRepository.get_all_categories()


def scan_category_is_valid(category_key: str) -> bool:
    """Check if Scan Category for such key exists.

    :param category_key: key representing Scan Category
    :return: boolean information if Scan Category key is valid
    """
    try:
        ScanCategoriesRepository.get_category_by_key(category_key)
        return True
    except NoResultFound:
        return False


def create_scan_category(key: str, name: str, image_path: str) -> ScanCategory:
    """Create new Scan ScanCategory.

    :param key: unique key representing Scan Category
    :param name: name which describes this Category
    :param image_path: path to the image which is located on the frontend
    :return: Scan Category object
    """
    return ScanCategoriesRepository.add_new_category(key, name, image_path)


def create_empty_scan(category_key: str, number_of_slices: int) -> Scan:
    """Create new empty scan.

    :param category_key: string with category key
    :param number_of_slices: number of Slices that will be uploaded
    :return: Newly created Scan object
    """
    category = ScanCategoriesRepository.get_category_by_key(category_key)
    return ScansRepository.add_new_scan(category, number_of_slices)


def get_metadata(scan_id: ScanID) -> ScanMetadata:
    """Fetch metadata for given scan.

    :param scan_id: ID of a given scan
    :return: Scan Metadata object
    """
    scan = ScansRepository.get_scan_by_id(scan_id)
    return ScanMetadata(scan_id=scan.id, number_of_slices=scan.number_of_slices)


def get_random_scan(category_key: str) -> ScanMetadata:
    """Fetch random scan for labeling.

    :param category_key: unique key identifying category
    :return: Scan Metadata object
    """
    category = ScanCategoriesRepository.get_category_by_key(category_key)
    scan = ScansRepository.get_random_scan(category)
    if not scan:
        raise NotFoundException('Could not find any Scan for this category!')

    return ScanMetadata(scan_id=scan.id, number_of_slices=scan.number_of_slices)


def get_slices_for_scan(scan_id: ScanID, begin: int, count: int,
                        orientation: SliceOrientation = SliceOrientation.Z) -> Iterable[Tuple[Slice, bytes]]:
    """Fetch multiple slices for given scan.

    :param scan_id: ID of a given scan
    :param begin: first slice index (included)
    :param count: number of slices that will be returned
    :param orientation: orientation for Slices (by default set to Z axis)
    :return: generator for Slices
    """
    slices = SlicesRepository.get_slices_by_scan_id(scan_id, orientation=orientation)
    for _slice in slices[begin:begin + count]:
        image = SlicesRepository.get_slice_converted_image(_slice.id)
        yield _slice, image


def add_label(scan_id: ScanID, selections: List[Dict]) -> Label:
    """Add label to given scan.

    :param scan_id: ID of a given scan
    :param selections: List of JSONs describing selections for a single label
    :return: Label object
    """
    label = LabelsRepository.add_new_label(scan_id)
    for selection in selections:
        position = LabelPosition(x=selection['x'], y=selection['y'], slice_index=selection['slice_index'])
        shape = LabelShape(width=selection['width'], height=selection['height'])
        binary_mask = LabelSelectionBinaryMask(selection['binary_mask']) if selection.get('binary_mask') else None
        LabelsRepository.add_new_label_selection(label.id, position, shape, binary_mask)
    return label


def add_new_slice(scan_id: ScanID, image: bytes) -> Slice:
    """Add new slice for given Scan.

    :param scan_id: ID of a Scan for which it should add new slice
    :param image: bytes representing Dicom image
    :return: Slice object
    """
    scan = ScansRepository.get_scan_by_id(scan_id)
    _slice = scan.add_slice()
    store_dicom.delay(_slice.id, image)

    # Run conversion to PNG if this is the latest uploaded Slice
    slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    if scan.number_of_slices == len(slices):  # Check if number of declared Slices is the same as number of Slices in DB
        convert_scan_to_png.delay(scan_id)
    return _slice


def get_scan(scan_id: ScanID) -> Scan:
    """Return Scan for given scan_id.

    :param scan_id: ID of a Scan which should be returned
    :return: Scan object
    """
    return ScansRepository.get_scan_by_id(scan_id)


def get_scan_metadata(scan_id: ScanID) -> ScanMetadata:
    """Return ScanMetadata for given scan_id.

    :param scan_id: ID of a Scan which should be returned
    :return: Scan Metadata object
    """
    scan = ScansRepository.get_scan_by_id(scan_id)
    return ScanMetadata(scan_id=scan.id, number_of_slices=scan.number_of_slices)
