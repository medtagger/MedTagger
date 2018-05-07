"""Module responsible for definition of Labels' Repository."""
from typing import List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import Label, LabelTag, User, LabelVerificationStatus, RectangularLabelElement
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
        with db_session() as session:
            label = session.query(Label).filter(Label.id == label_id).one()
        return label

    @staticmethod
    def get_random_label(status: LabelVerificationStatus = None) -> Label:
        """Fetch random Label from database.

        :param status: (optional) verification status for Label
        :return: Label object
        """
        with db_session() as session:
            query = session.query(Label)
            if status:
                query = query.filter(Label.status == status)
            query = query.order_by(func.random())
            label = query.first()
        return label

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
        :param shape: shape (width, height, depth) of the Label
        :param label_tag: Label Tag object
        :return: ID of a Element
        """
        with db_session() as session:
            new_rectangular_label_element = RectangularLabelElement(position, shape, label_tag)
            new_rectangular_label_element.label_id = label_id
            session.add(new_rectangular_label_element)

        return new_rectangular_label_element.id
