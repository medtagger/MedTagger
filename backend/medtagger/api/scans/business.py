"""Module responsible for business logic in all Scans endpoints."""
import io
import logging
from typing import Callable, Iterable, Dict, List, Tuple, Any

from cassandra import WriteTimeout
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from PIL import Image

from medtagger.api.exceptions import NotFoundException, InvalidArgumentsException, InternalErrorException
from medtagger.types import ScanID, LabelPosition, LabelShape, LabelingTime, LabelID, Point
from medtagger.database.models import ScanCategory, Scan, Slice, Label, LabelTag, SliceOrientation
from medtagger.definitions import LabelTool
from medtagger.repositories import (
    labels as LabelsRepository,
    label_tags as LabelTagsRepository,
    slices as SlicesRepository,
    scans as ScansRepository,
    scan_categories as ScanCategoriesRepository,
    tasks as TasksRepository,
)
from medtagger.workers.storage import parse_dicom_and_update_slice
from medtagger.api.utils import get_current_user

logger = logging.getLogger(__name__)

LabelElementHandler = Callable[[Dict[str, Any], LabelID, Dict[str, bytes]], None]


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


def create_scan_category(key: str, name: str) -> ScanCategory:
    """Create new Scan ScanCategory.

    :param key: unique key representing Scan Category
    :param name: name which describes this Category
    :return: Scan Category object
    """
    return ScanCategoriesRepository.add_new_category(key, name)


def create_empty_scan(category_key: str, declared_number_of_slices: int) -> Scan:
    """Create new empty scan.

    :param category_key: string with category key
    :param declared_number_of_slices: number of Slices that will be uploaded
    :return: Newly created Scan object
    """
    user = get_current_user()
    category = ScanCategoriesRepository.get_category_by_key(category_key)
    return ScansRepository.add_new_scan(category, declared_number_of_slices, user)


def get_random_scan(task_key: str) -> Scan:
    """Fetch random scan from specified Task for labeling.

    :param task_key: unique key identifying task
    :return: Scan Metadata object
    """
    user = get_current_user()
    task = TasksRepository.get_task_by_key(task_key)
    if not task:
        raise InvalidArgumentsException('Task key {} is invalid!'.format(task_key))
    scan = ScansRepository.get_random_scan(task, user)
    if not scan:
        raise NotFoundException('Could not find any Scan for this task!')
    return scan


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


def validate_label_payload(elements: List[Dict], files: Dict[str, bytes]) -> None:
    """Validate and raise an Exception for sent payload.

    :param elements: List of JSONs describing elements for a single label
    :param files: mapping of uploaded files (name and content)
    """
    _validate_files(files)
    _validate_label_elements(elements, files)
    _validate_tool(elements)


def _validate_tool(elements: List[Dict]) -> None:
    """Validate if the tool for given Label Element is available for given tag."""
    for label_element in elements:
        tag = _get_label_tag(label_element['tag'])
        if label_element['tool'] not in {tool.name for tool in tag.tools}:
            raise InvalidArgumentsException('{} tool is not available for {} tag'.format(
                label_element['tool'], tag.name))


def _validate_files(files: Dict[str, bytes]) -> None:
    """Validate files and make sure that images are PNGs."""
    for file_name, file_data in files.items():
        try:
            image = Image.open(io.BytesIO(file_data))
            image.verify()
            assert image.format == 'PNG'
        except Exception:
            raise InvalidArgumentsException('Type of file "{}" is not supported!'.format(file_name))


def _validate_label_elements(elements: List[Dict], files: Dict[str, bytes]) -> None:
    """Validate Label Elements and make sure that all Brush Elements have images."""
    for label_element in elements:
        # Each Brush Label Element should have its own image attached
        if label_element['tool'] == LabelTool.BRUSH.value:
            try:
                files[label_element['image_key']]
            except KeyError:
                message = 'Request does not have field named {} that could contain the image!'
                raise InvalidArgumentsException(message.format(label_element['image_key']))


def add_label(scan_id: ScanID, task_key: str, elements: List[Dict], files: Dict[str, bytes],
              labeling_time: LabelingTime, comment: str = None) -> Label:   # pylint: disable=too-many-arguments
    """Add label to given scan.

    :param scan_id: ID of a given scan
    :param task_key: Key of Task
    :param elements: List of JSONs describing elements for a single label
    :param files: mapping of uploaded files (name and content)
    :param labeling_time: time in seconds that user spent on labeling
    :param comment: (optional) comment describing a label
    :return: Label object
    """
    user = get_current_user()
    try:
        label = LabelsRepository.add_new_label(scan_id, task_key, user, labeling_time, comment)
    except IntegrityError:
        raise NotFoundException('Could not find Scan for that id!')
    for element in elements:
        add_label_element(element, label.id, files)
    return label


def add_label_element(element: Dict[str, Any], label_id: LabelID, files: Dict[str, bytes]) -> None:
    """Add new Label Element for given Label.

    :param element: JSON describing single element
    :param label_id: ID of a given Label that the element should be added to
    :param files: mapping of uploaded files (name and content)
    """
    tool = element['tool']
    handlers: Dict[str, LabelElementHandler] = {
        LabelTool.RECTANGLE.value: _add_rectangle_element,
        LabelTool.BRUSH.value: _add_brush_element,
        LabelTool.POINT.value: _add_point_element,
        LabelTool.CHAIN.value: _add_chain_element,
    }
    handler = handlers[tool]
    handler(element, label_id, files)


def _add_rectangle_element(element: Dict[str, Any], label_id: LabelID, *_: Any) -> None:
    """Add new Rectangular Label Element for given Label.

    :param element: JSON describing single element
    :param label_id: ID of a given Label that the element should be added to
    """
    position = LabelPosition(x=element['x'], y=element['y'], slice_index=element['slice_index'])
    shape = LabelShape(width=element['width'], height=element['height'])
    label_tag = _get_label_tag(element['tag'])
    LabelsRepository.add_new_rectangular_label_element(label_id, position, shape, label_tag)


def _add_brush_element(element: Dict[str, Any], label_id: LabelID, files: Dict[str, bytes]) -> None:
    """Add new Brush Label Element for given Label.

    :param element: JSON describing single element
    :param label_id: ID of a given Label that the element should be added to
    :param files: mapping of uploaded files (name and content)
    """
    width = element['width']
    height = element['height']
    label_tag = _get_label_tag(element['tag'])
    slice_index = element['slice_index']
    image = files[element['image_key']]
    LabelsRepository.add_new_brush_label_element(label_id, slice_index, width, height, image, label_tag)


def _add_point_element(element: Dict[str, Any], label_id: LabelID, *_: Any) -> None:
    """Add new Point Label Element for given Label.

    :param element: JSON describing single element
    :param label_id: ID of a given Label that the element should be added to
    """
    position = LabelPosition(x=element['x'], y=element['y'], slice_index=element['slice_index'])
    label_tag = _get_label_tag(element['tag'])
    LabelsRepository.add_new_point_label_element(label_id, position, label_tag)


def _add_chain_element(element: Dict[str, Any], label_id: LabelID, *_: Any) -> None:
    """Add new Chain Label Element for given Label.

    :param element: JSON describing single element
    :param label_id: ID of a given Label that the element should be added to
    """
    label_tag = _get_label_tag(element['tag'])
    points = [Point(p['x'], p['y']) for p in element['points']]
    slice_index = element['slice_index']
    loop = element['loop']
    LabelsRepository.add_new_chain_label_element(label_id, slice_index, label_tag, points, loop)


def _get_label_tag(tag_key: str) -> LabelTag:
    """Return Label Tag based on Tag's key or raise an exception in case if not found."""
    try:
        return LabelTagsRepository.get_label_tag_by_key(tag_key)
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
    try:
        SlicesRepository.store_original_image(_slice.id, image)
    except WriteTimeout:
        SlicesRepository.delete_slice_by_id(_slice.id)
        raise InternalErrorException('Timeout during saving original image to the Storage.')
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


def skip_scan(scan_id: ScanID) -> bool:
    """Increases skip count of Scan with given scan_id.

    :param scan_id: ID of a Scan which should be returned
    :return: boolean information whether the Scan was skipped or not
    """
    if not ScansRepository.increase_skip_count_of_a_scan(scan_id):
        raise NotFoundException('Scan "{}" not found.'.format(scan_id))
    return True
