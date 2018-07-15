"""Tests survey system."""
import json
from typing import Any

from medtagger.database.models import Survey, SurveySingleChoiceQuestion
from medtagger.types import SurveyElementKey

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user
from tests.functional_tests.helpers import create_tag_and_assign_to_task


def test_adding_new_survey(prepare_environment: Any) -> None:
    """Test for adding new Survey and fetching it through API."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('volunteer')

    # Add an example of Survey
    survey = Survey(name='Colors Survey', initial_element_key=SurveyElementKey('FIRST_QUESTION'))
    survey.elements = [
        SurveySingleChoiceQuestion(
            key=SurveyElementKey('FIRST_QUESTION'),
            title='What is your favourite color?',
            possible_answers={
                'Red': SurveyElementKey('SECOND_QUESTION'),
                'Green': None,
                'Blue': None,
            },
        ),
        SurveySingleChoiceQuestion(
            key=SurveyElementKey('SECOND_QUESTION'),
            title='Why do you like Red?',
            possible_answers={
                'It is nice': None,
                'Love it': None,
                'I do not know': None,
            },
        ),
    ]
    survey.save()

    # Assign above Survey to an Example Tag available for MARK_KIDNEYS Task
    label_tag = create_tag_and_assign_to_task('EXAMPLE_TAG', 'Example tag', 'MARK_KIDNEYS')
    label_tag.actions.append(survey)
    label_tag.save()

    # Check if it's available through API
    response = api_client.get('/api/v1/labels/actions/1', headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert set(json_response) == {'action_id', 'action_type', 'details'}
    assert json_response['action_id'] == 1
    assert json_response['action_type'] == 'Survey'
    assert isinstance(json_response['details'], dict)

    # Make sure that Survey details have all necessary fields
    assert set(json_response['details']) == {'name', 'initial_element_key', 'elements'}
    assert json_response['details']['name'] == 'Colors Survey'
    assert json_response['details']['initial_element_key'] == 'FIRST_QUESTION'
    assert isinstance(json_response['details']['elements'], list)

    # Check what elements does this Survey contain
    all_elements = json_response['details']['elements']
    assert len(all_elements) == 2
    all_element_keys = {element['key'] for element in all_elements}
    assert all_element_keys == {'FIRST_QUESTION', 'SECOND_QUESTION'}

    # Check what does first question has inside
    first_question = next(element for element in all_elements if element['key'] == 'FIRST_QUESTION')
    assert first_question == {
        'key': 'FIRST_QUESTION',
        'instant_next_element': None,
        'type': 'SurveySingleChoiceQuestion',
        'title': 'What is your favourite color?',
        'possible_answers': {
            'Red': 'SECOND_QUESTION',
            'Green': None,
            'Blue': None,
        },
    }

    # And what second question has inside
    first_question = next(element for element in all_elements if element['key'] == 'SECOND_QUESTION')
    assert first_question == {
        'key': 'SECOND_QUESTION',
        'instant_next_element': None,
        'type': 'SurveySingleChoiceQuestion',
        'title': 'Why do you like Red?',
        'possible_answers': {
            'It is nice': None,
            'Love it': None,
            'I do not know': None,
        },
    }

    # Check if we can fetch any unavailable Action through API
    response = api_client.get('/api/v1/labels/actions/2', headers=get_headers(token=user_token))
    assert response.status_code == 404
    json_response = json.loads(response.data)
    assert json_response == {
        'message': 'Requested object does not exist.',
        'details': 'Action "2" not found.',
    }

    # Check if above Action is available from Task endpoint
    response = api_client.get('/api/v1/scans/tasks', headers=get_headers(token=user_token))
    json_response = json.loads(response.data)
    mark_kidneys_task = next(task for task in json_response if task['key'] == 'MARK_KIDNEYS')
    example_tag = next(tag for tag in mark_kidneys_task['tags'] if tag['key'] == 'EXAMPLE_TAG')
    assert example_tag['actions_ids'] == [1]


def test_adding_new_response_for_survey(prepare_environment: Any) -> None:
    """Test for adding new Response for Survey."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('volunteer')

    # Add an example of Survey
    survey = Survey(name='Colors Survey', initial_element_key=SurveyElementKey('FIRST_QUESTION'))
    survey.elements = [
        SurveySingleChoiceQuestion(
            key=SurveyElementKey('FIRST_QUESTION'),
            title='What is your favourite color?',
            possible_answers={
                'Red': SurveyElementKey('SECOND_QUESTION'),
                'Green': None,
                'Blue': None,
            },
        ),
        SurveySingleChoiceQuestion(
            key=SurveyElementKey('SECOND_QUESTION'),
            title='Why do you like Red?',
            possible_answers={
                'It is nice': None,
                'Love it': None,
                'I do not know': None,
            },
        ),
    ]
    survey.save()

    # Check if user can post a Response through API
    payload = {'FIRST_QUESTION': 'Red', 'SECOND_QUESTION': 'Love it'}
    response = api_client.post('/api/v1/labels/actions/1', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert json_response == {
        'action_id': 1,
        'action_type': 'Survey',
        'response_id': 1,
        'details': {
            'FIRST_QUESTION': 'Red',
            'SECOND_QUESTION': 'Love it',
        },
    }

    # Check if user can post invalid Response (keys that were not in Survey)
    payload = {'FIRST_QUESTION': 'Red', 'THIRD_QUESTION': 'I am a hacker!'}
    response = api_client.post('/api/v1/labels/actions/1', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 400
    json_response = json.loads(response.data)
    assert json_response == {
        'message': 'Invalid arguments.',
        'details': 'Your answers does not match keys in Survey.',
    }
