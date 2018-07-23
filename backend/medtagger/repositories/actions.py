"""Module responsible for definition of ActionsRepository."""
from typing import Dict, cast

from medtagger.database import db_session
from medtagger.database.models import Action, ActionResponse, SurveyResponse
from medtagger.exceptions import UnsupportedActionException, InvalidResponseException
from medtagger.types import ActionID, SurveyID


def get_action_by_id(action_id: ActionID) -> Action:
    """Fetch Action from database."""
    return Action.query.filter(Action.id == action_id).one()


def add_action_response(action_id: ActionID, response: Dict) -> ActionResponse:
    """Add response for given Action."""
    action = Action.query.filter(Action.id == action_id).one()
    if action.action_type == 'Survey':
        valid = action.validate_response(response)
        if not valid:
            raise InvalidResponseException('Your answers does not match keys in Survey.')
        with db_session() as session:
            survey_id = cast(SurveyID, action_id)
            action_response = SurveyResponse(survey_id, response)
            session.add(action_response)
    else:
        raise UnsupportedActionException('Action does not support returning Respose.')
    return action_response
