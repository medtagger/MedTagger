"""Module responsible for business logic in all Scans endpoints."""
import logging
from typing import Iterable, Dict, List, Tuple, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from medtagger.api.exceptions import NotFoundException, InvalidArgumentsException
from medtagger.repositories.label_tag import LabelTagRepository
from medtagger.types import ScanID, LabelPosition, LabelShape, ScanMetadata, LabelingTime, LabelID
from medtagger.database.models import ScanCategory, Scan, Slice, Label, SliceOrientation, LabelTool
from medtagger.repositories.labels import LabelsRepository
from medtagger.repositories.slices import SlicesRepository
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.scan_categories import ScanCategoriesRepository
from medtagger.workers.storage import parse_dicom_and_update_slice
from medtagger.api.utils import get_current_user

logger = logging.getLogger(__name__)


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


def create_empty_scan(category_key: str, declared_number_of_slices: int) -> Scan:
    """Create new empty scan.

    :param category_key: string with category key
    :param declared_number_of_slices: number of Slices that will be uploaded
    :return: Newly created Scan object
    """
    user = get_current_user()
    category = ScanCategoriesRepository.get_category_by_key(category_key)
    return ScansRepository.add_new_scan(category, declared_number_of_slices, user)


def get_metadata(scan_id: ScanID) -> ScanMetadata:
    """Fetch metadata for given scan.

    :param scan_id: ID of a given scan
    :return: Scan Metadata object
    """
    scan = ScansRepository.get_scan_by_id(scan_id)
    return ScanMetadata(scan_id=scan.id, number_of_slices=scan.declared_number_of_slices)


def get_random_scan(category_key: str) -> ScanMetadata:
    """Fetch random scan for labeling.

    :param category_key: unique key identifying category
    :return: Scan Metadata object
    """
    user = get_current_user()
    category = ScanCategoriesRepository.get_category_by_key(category_key)
    scan = ScansRepository.get_random_scan(category, user)
    if not scan:
        raise NotFoundException('Could not find any Scan for this category!')

    return ScanMetadata(scan_id=scan.id, number_of_slices=scan.declared_number_of_slices)


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


def add_label(scan_id: ScanID, elements: List[Dict], labeling_time: LabelingTime) -> Label:
    """Add label to given scan.

    :param scan_id: ID of a given scan
    :param elements: List of JSONs describing elements for a single label
    :param labeling_time: time in seconds that user spent on labeling
    :return: Label object
    """
    user = get_current_user()
    try:
        label = LabelsRepository.add_new_label(scan_id, user, labeling_time)
    except IntegrityError:
        raise NotFoundException('Could not find Scan for that id!')
    for element in elements:
        add_label_element(element, label.id)
    return label


def add_label_element(element: Dict[str, Any], label_id: LabelID) -> None:
    """Add new Label Element for given Label.

    :param element: JSON describing single element
    :param label_id: ID of a given Label that the element should be added to
    """
    tool = element['tool']
    if tool == LabelTool.RECTANGLE.value:
        position = LabelPosition(x=element['x'], y=element['y'], slice_index=element['slice_index'])
        shape = LabelShape(width=element['width'], height=element['height'])
        try:
            label_tag = LabelTagRepository.get_label_tag_by_key(element['tag'])
        except NoResultFound:
            raise NotFoundException('Could not find any Label Tag for that key!')
        LabelsRepository.add_new_rectangular_label_element(label_id, position, shape, label_tag)
    else:
        raise InvalidArgumentsException('That tool is not supported!')


def add_new_slice(scan_id: ScanID, image: bytes) -> Slice:
    """Add new Slice for given Scan.

    :param scan_id: ID of a Scan for which it should add new slice
    :param image: bytes representing Dicom image
    :return: Slice object
    """
    scan = ScansRepository.get_scan_by_id(scan_id)
    _slice = scan.add_slice()
    SlicesRepository.store_original_image(_slice.id, image)
    parse_dicom_and_update_slice.delay(_slice.id)
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
    return ScanMetadata(scan_id=scan.id, number_of_slices=scan.declared_number_of_slices)
