"""Module responsible for business logic in all Labels endpoints."""
from sqlalchemy.orm.exc import NoResultFound

from medtagger.types import LabelID
from medtagger.api.exceptions import NotFoundException
from medtagger.database.models import Label, LabelVerificationStatus
from medtagger.repositories.labels import LabelsRepository


def change_label_status(label_id: LabelID, status: LabelVerificationStatus) -> Label:
    """Change status of the label.

    :param label_id: ID of a label for which the status should be changed
    :param status: new Label Verification Status that should be set
    """
    try:
        label = LabelsRepository.get_label_by_id(label_id)
    except NoResultFound:
        raise NotFoundException('Label "{}" not found.'.format(label_id))

    label.update_status(status)
    return label


def get_random_label() -> Label:
    """Fetch random label that has the NOT_VERIFIED status.

    :return: dictionary with details about label
    """
    try:
        return LabelsRepository.get_random_label(LabelVerificationStatus.NOT_VERIFIED)
    except NoResultFound:
        raise NotFoundException('No Labels not found.')
