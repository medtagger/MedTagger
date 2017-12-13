"""Module responsible for definition of Labels' Repository"""
from sqlalchemy.sql.expression import func

from data_labeling.database import db_session
from data_labeling.database.models import Label, LabelStatus
from data_labeling.types import LabelID, ScanID


class LabelsRepository(object):
    """Repository for Labels"""

    @staticmethod
    def get_label_by_id(label_id: LabelID) -> Label:
        """Fetch Label from database"""
        with db_session() as session:
            label = session.query(Label).filter(Label.id == label_id).one()
        return label

    @staticmethod
    def get_random_label(status: LabelStatus = None) -> Label:
        """Fetch random Label from database

        :param status: (optional) status for Label
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
    def add_new_label(scan_id: ScanID) -> Label:
        """Add new Label for given Scan"""
        with db_session() as session:
            label = Label()
            label.scan_id = scan_id
            session.add(label)
        return label
