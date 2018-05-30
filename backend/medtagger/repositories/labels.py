"""Module responsible for definition of Labels' Repository."""
from typing import List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import Label, LabelTag, User, RectangularLabelElement, BrushLabelElement
from medtagger.definitions import LabelVerificationStatus
from medtagger.storage.models import BrushLabelElement as BrushLabelElementStorage
from medtagger.types import LabelID, LabelPosition, LabelShape, LabelElementID, ScanID, LabelingTime


class LabelsRepository(object):
    """Repository for Labels."""

    @staticmethod
    def get_all_labels() -> List[Label]:
        """Fetch all Labels from database."""
        return Label.query.all()

    @staticmethod
    def get_label_by_id(label_id: LabelID) -> Label:
        """Fetch Label from database."""
        return Label.query.filter(Label.id == label_id).one()

    @staticmethod
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

    @staticmethod
    def add_new_label(scan_id: ScanID, user: User, labeling_time: LabelingTime) -> Label:
        """Add new Label for given Scan."""
        with db_session() as session:
            label = Label(user, labeling_time)
            label.scan_id = scan_id
            session.add(label)
        return label

    @staticmethod
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

    @staticmethod
    def add_new_brush_label_element(label_id: LabelID, slice_index: int, width: int, height: int, image: bytes,
                                    label_tag: LabelTag) -> LabelElementID:
        """Add new Brush Element for given Label.

        :param label_id: Label's ID
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
