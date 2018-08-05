"""Module responsible for definition of LabelsRepository."""
from typing import List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import Label, LabelTag, User, RectangularLabelElement, BrushLabelElement, \
    PointLabelElement, ChainLabelElement, ChainLabelElementPoint, Task
from medtagger.definitions import LabelVerificationStatus
from medtagger.storage.models import BrushLabelElement as BrushLabelElementStorage
from medtagger.types import LabelID, LabelPosition, LabelShape, LabelElementID, ScanID, LabelingTime, Point


def get_all_labels() -> List[Label]:
    """Fetch all Labels from database."""
    return Label.query.all()


def get_label_by_id(label_id: LabelID) -> Label:
    """Fetch Label from database."""
    return Label.query.filter(Label.id == label_id).one()


def get_random_label(status: LabelVerificationStatus = None) -> Label:
    """Fetch random Label from database.

    :param status: (optional) verification status for Label
    :return: Label object
    """
    query = Label.query
    if status:
        query = query.filter(Label.status == status)
    query = query.order_by(func.random())
    return query.first()


def add_new_label(scan_id: ScanID, task_key: str, user: User, labeling_time: LabelingTime, comment: str = None) -> Label:
    """Add new Label for given Scan."""
    with db_session() as session:
        label = Label(user, labeling_time, comment)
        label.scan_id = scan_id
        label.task = Task.query.filter(Task.key == task_key).one()
        session.add(label)
    return label


def add_new_rectangular_label_element(label_id: LabelID, position: LabelPosition, shape: LabelShape,
                                      label_tag: LabelTag) -> LabelElementID:
    """Add new Rectangular Element for given Label.

    :param label_id: Label's ID
    :param position: position (x, y, slice_index) of the Label
    :param shape: shape (width, height) of the Label
    :param label_tag: Label Tag object
    :return: ID of a Element
    """
    with db_session() as session:
        rectangular_label_element = RectangularLabelElement(position, shape, label_tag)
        rectangular_label_element.label_id = label_id
        session.add(rectangular_label_element)

    return rectangular_label_element.id


def add_new_brush_label_element(label_id: LabelID, slice_index: int, width: int, height: int, image: bytes,
                                label_tag: LabelTag) -> LabelElementID:
    """Add new Brush Element for given Label.

    :param label_id: Label's ID
    :param slice_index: index of Slice
    :param width: width of the Label's image
    :param height: height of the Label's image
    :param image: bytes with image representation of a binary mask
    :param label_tag: Label Tag object
    :return: ID of a Element
    """  # pylint: disable=too-many-arguments
    with db_session() as session:
        brush_label_element = BrushLabelElement(slice_index, width, height, label_tag)
        brush_label_element.label_id = label_id
        session.add(brush_label_element)
    BrushLabelElementStorage.create(id=brush_label_element.id, image=image)
    return brush_label_element.id


def add_new_point_label_element(label_id: LabelID, position: LabelPosition, label_tag: LabelTag) -> LabelElementID:
    """Add new Point Element for given Label.

    :param label_id: Label's ID
    :param position: position (x, y, slice_index) of the Label
    :param label_tag: Label Tag object
    :return: ID of a Element
    """
    with db_session() as session:
        point_label_element = PointLabelElement(position, label_tag)
        point_label_element.label_id = label_id
        session.add(point_label_element)

    return point_label_element.id


def add_new_chain_label_element(label_id: LabelID, slice_index: int, label_tag: LabelTag, points: List[Point],
                                loop: bool) -> LabelElementID:
    """Add new Chain Element for given Label.

    :param label_id: Label's ID
    :param slice_index: Slice's index
    :param label_tag: Label Tag object
    :param points: array of points where points with consecutive indices are connected
    :param loop: true if first and last points are connected
    :return: ID of a Element
    """
    with db_session() as session:
        chain_label_element = ChainLabelElement(slice_index, label_tag, loop)
        chain_label_element.label_id = label_id
        session.add(chain_label_element)

        for order, point in enumerate(points):
            chain_label_element_point = ChainLabelElementPoint(point.x, point.y, chain_label_element.id, order)
            session.add(chain_label_element_point)

    return chain_label_element.id
