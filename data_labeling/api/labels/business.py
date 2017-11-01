"""Module responsible for business logic in all Labels endpoints"""
from typing import Dict, Any

from sqlalchemy.sql.expression import func

from data_labeling.types import LabelID
from data_labeling.database import db_session
from data_labeling.database.models import Label, LabelStatus


def change_label_status(label_id: LabelID, status: str) -> Label:
    """Change status of the label

    :param label_id: ID of a label for which the status should be changed
    :param status: new status for the label
    """
    with db_session() as session:
        label = session.query(Label).filter(Label.id == label_id).one()
        label.status = status
    return label


def get_random_label() -> Dict[str, Any]:
    """Fetch random label that has the NOT_VERIFIED status

    :return: dictionary with details about label
    """
    with db_session() as session:
        label = session.query(Label).filter(Label.status == LabelStatus.NOT_VERIFIED).order_by(func.random()).first()

    return label
