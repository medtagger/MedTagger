"""Module responsible for business logic in all Labels endpoints."""
from typing import Dict

from sqlalchemy.orm.exc import NoResultFound

from medtagger.types import LabelID, ActionID
from medtagger.api.exceptions import NotFoundException, InvalidArgumentsException
from medtagger.database.models import Label, LabelStatus, Action, ActionResponse
from medtagger.repositories.labels import LabelsRepository
from medtagger.repositories.actions import ActionsRepository, InvalidResponseException, \
    UnsupportedActionException


def change_label_status(label_id: LabelID, status: LabelStatus) -> Label:
    """Change status of the Label.

    :param label_id: ID of a Label for which the status should be changed
    :param status: new Label Status that should be set
    :return: Label that was changed
    """
    try:
        label = LabelsRepository.get_label_by_id(label_id)
    except NoResultFound:
        raise NotFoundException('Label with ID={} not found.'.format(label_id))

    label.update_status(status)
    return label


def get_random_label() -> Label:
    """Fetch random label that has the NOT_VERIFIED status.

    :return: random Label object from database
    """
    try:
        return LabelsRepository.get_random_label(LabelStatus.NOT_VERIFIED, fetch_binary_masks=True)
    except NoResultFound:
        raise NotFoundException('No Labels found.')


def get_action_details(action_id: ActionID) -> Action:
    """Fetch details about Action.

    :param action_id: ID of an Action that should be returned
    :return: Action for given ID
    """
    try:
        return ActionsRepository.get_action_by_id(action_id)
    except NoResultFound:
        raise NotFoundException('Action "{}" not found.'.format(action_id))


def add_action_response(action_id: ActionID, response: Dict) -> ActionResponse:
    """Add new Response for given Action.

    :param action_id: ID of an Action for which this Response should be added
    :param response: dictionary Response for given Action
    :return: ActionResponse database object
    """
    try:
        return ActionsRepository.add_action_response(action_id, response)
    except NoResultFound:
        raise NotFoundException('Action "{}" not found.'.format(action_id))
    except UnsupportedActionException:
        raise InvalidArgumentsException('Action does not support returning Respose.')
    except InvalidResponseException:
        raise InvalidArgumentsException('Your answers does not match keys in Survey.')
