"""Module responsible for business logic in all Scans endpoints."""
import logging
from typing import Iterable, Mapping, Dict, List, Tuple, Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.datastructures import FileStorage

from medtagger.api.exceptions import NotFoundException, InvalidArgumentsException
from medtagger.repositories.label_tag import LabelTagRepository
from medtagger.types import ScanID, LabelPosition, LabelShape, LabelingTime, LabelID
from medtagger.database.models import ScanCategory, Scan, Slice, Label, LabelTag, SliceOrientation
from medtagger.definitions import LabelTool
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


def get_random_scan(category_key: str) -> Scan:
    """Fetch random scan for labeling.

    :param category_key: unique key identifying category
    :return: Scan Metadata object
    """
    user = get_current_user()
    category = ScanCategoriesRepository.get_category_by_key(category_key)
    try:
        scan = ScansRepository.get_random_scan(category, user)
        if not scan:
            raise NotFoundException('Could not find any Scan for this category!')
        return scan
    except NoResultFound:
        raise NotFoundException('Could not find any Scan for this category!')


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


def add_label(scan_id: ScanID, elements: List[Dict], files: Dict[str, FileStorage], labeling_time: LabelingTime) -> Label:
    """Add label to given scan.

    :param scan_id: ID of a given scan
    :param elements: List of JSONs describing elements for a single label
    :param files: mapping of uploaded files (name and content)
    :param labeling_time: time in seconds that user spent on labeling
    :return: Label object
    """
    user = get_current_user()
    try:
        label = LabelsRepository.add_new_label(scan_id, user, labeling_time)
    except IntegrityError:
        raise NotFoundException('Could not find Scan for that id!')
    for element in elements:
        add_label_element(element, files, label.id)
    return label


def add_label_element(element: Dict[str, Any], files: Dict[str, FileStorage], label_id: LabelID) -> None:
    """Add new Label Element for given Label.

    :param element: JSON describing single element
    :param files: mapping of uploaded files (name and content)
    :param label_id: ID of a given Label that the element should be added to
    """
    tool = element['tool']
    handlers = {
        LabelTool.RECTANGLE.value: _add_rectangle_element,
        LabelTool.BRUSH.value: _add_brush_element,
    }
    try:
        handler = handlers[tool]
        handler(element, files, label_id)
    except KeyError:
        raise InvalidArgumentsException('{} tool is not supported!'.format(tool))


def _add_rectangle_element(element: Dict[str, Any], files: Dict[str, FileStorage], label_id: LabelID) -> None:
    """Add new Rectangular Label Element for given Label.

    :param element: JSON describing single element
    :param files: (not used) mapping of uploaded files (name and content)
    :param label_id: ID of a given Label that the element should be added to
    """
    position = LabelPosition(x=element['x'], y=element['y'], slice_index=element['slice_index'])
    shape = LabelShape(width=element['width'], height=element['height'])
    label_tag = _get_label_tag(element['tag'])
    LabelsRepository.add_new_rectangular_label_element(label_id, position, shape, label_tag)


def _add_brush_element(element: Dict[str, Any], files: Dict[str, FileStorage], label_id: LabelID) -> None:
    """Add new Brush Label Element for given Label.

    :param element: JSON describing single element
    :param files: mapping of uploaded files (name and content)
    :param label_id: ID of a given Label that the element should be added to
    """
    shape = LabelShape(width=element['width'], height=element['height'])
    label_tag = _get_label_tag(element['tag'])
    slice_index = element['slice_index']
    image = files[element['image_key']].read()
    LabelsRepository.add_new_brush_label_element(label_id, slice_index, shape, image, label_tag)


def _get_label_tag(tag_key: str) -> LabelTag:
    """Return Label Tag based on Tag's key or raise an exception in case if not found."""
    try:
        return LabelTagRepository.get_label_tag_by_key(tag_key)
    except NoResultFound:
        raise NotFoundException('Could not find any Label Tag for that key!')


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
    try:
        return ScansRepository.get_scan_by_id(scan_id)
    except NoResultFound:
        raise NotFoundException('Scan "{}" not found.'.format(scan_id))
