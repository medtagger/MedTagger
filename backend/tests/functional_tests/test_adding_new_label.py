"""Tests for adding new Labels to the system."""
import json
from typing import Any

from medtagger.storage.models import BrushLabelElement

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user
from tests.functional_tests.helpers import create_tag_and_assign_to_category


def test_add_brush_label(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test for adding a Label made with Brush tool."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Add Scan to the system
    payload = {'category': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 2. Label it with Brush
    create_tag_and_assign_to_category('EXAMPLE_TAG', 'Example tag', 'KIDNEYS')
    payload = {
        'elements': [{
            'slice_index': 0,
            'width': 128,
            'height': 128,
            'image_key': 'SLICE_1',
            'tag': 'EXAMPLE_TAG',
            'tool': 'BRUSH',
        }],
        'labeling_time': 12.34,
    }
    with open('tests/assets/example_labels/binary_mask.png', 'rb') as image:
        data = {
            'label': json.dumps(payload),
            'SLICE_1': (image, 'slice_1'),
        }
        response = api_client.post('/api/v1/scans/{}/label'.format(scan_id), data=data,
                                   headers=get_headers(token=user_token, multipart=True))
    assert response.status_code == 201
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_id = json_response['label_id']
    assert isinstance(label_id, str)
    assert len(label_id) >= 1

    # Step 3. Fetch details about above Label and check image storage
    response = api_client.get('/api/v1/labels/' + label_id, headers=get_headers(token=user_token))
    assert response.status_code == 200
    json_response = json.loads(response.data)
    assert isinstance(json_response, dict)
    label_element_id = json_response['elements'][0]['label_element_id']
    brush_label_element = BrushLabelElement.get(id=label_element_id)
    assert brush_label_element.image
