"""Tests for Scan upload to the system."""
import io
import glob
import json
from typing import Any

import pytest
from cassandra import WriteTimeout
from PIL import Image

from medtagger.database.models import SliceOrientation
from medtagger.repositories import (
    slices as SlicesRepository,
    scan_categories as ScanCategoriesRepository
)

from tests.functional_tests import get_api_client, get_headers
from tests.functional_tests.conftest import get_token_for_logged_in_user


# pylint: disable=too-many-locals
def test_scan_upload_and_conversion(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application for Scan upload and conversion."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    ScanCategoriesRepository.add_new_category('KIDNEYS', 'Kidneys')

    # Step 2. Add Scan to the system
    payload = {'category': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Send Slices
    for file in glob.glob('tests/assets/example_scan/*.dcm'):
        with open(file, 'rb') as image:
            response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
                'image': (image, 'slice_1.dcm'),
            }, headers=get_headers(token=user_token, multipart=True))
            assert response.status_code == 201

    # Step 4. Check Scan & Slices in the databases
    z_slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    assert len(z_slices) == 3
    y_slices = SlicesRepository.get_slices_by_scan_id(scan_id, SliceOrientation.Y)
    assert not y_slices
    x_slices = SlicesRepository.get_slices_by_scan_id(scan_id, SliceOrientation.X)
    assert not x_slices

    # Step 5.1. Slices in Z axis
    z_slice = SlicesRepository.get_slice_converted_image(z_slices[2].id)
    z_slice_image = Image.open(io.BytesIO(z_slice))
    assert z_slice_image.size == (512, 512)

    # Step 5.2. Slices in Y axis are disabled for now
    # y_slice = SlicesRepository.get_slice_converted_image(y_slices[128].id)
    # y_slice_image = Image.open(io.BytesIO(y_slice))
    # assert y_slice_image.size == (256, 186)

    # Step 5.3. Slices in Z axis are disabled for now
    # x_slice = SlicesRepository.get_slice_converted_image(x_slices[128].id)
    # x_slice_image = Image.open(io.BytesIO(x_slice))
    # assert x_slice_image.size == (256, 186)


@pytest.fixture
def fixture_problems_with_storage(mocker: Any) -> Any:
    """Fixture that mocks method related to storing original image in Cassandra."""
    return mocker.patch.object(SlicesRepository, 'store_original_image')


def test_scan_upload_with_retrying(fixture_problems_with_storage: Any, prepare_environment: Any,
                                   synchronous_celery: Any) -> None:
    """Test application for Scan upload with retrying."""
    api_client = get_api_client()
    user_token = get_token_for_logged_in_user('admin')

    # Step 1. Prepare a structure for the test
    ScanCategoriesRepository.add_new_category('KIDNEYS', 'Kidneys')

    # Step 2. Add Scan to the system
    payload = {'category': 'KIDNEYS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload),
                               headers=get_headers(token=user_token, json=True))
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 3. Send Slices
    for file in glob.glob('tests/assets/example_scan/*.dcm'):
        with open(file, 'rb') as image:
            # First request to the API will fail with unknown error due to Storage issues
            fixture_problems_with_storage.side_effect = WriteTimeout('Internal Storage Error', write_type=0)
            response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
                'image': (image, 'slice_1.dcm'),
            }, headers=get_headers(token=user_token, multipart=True))
            assert response.status_code == 500

            # After such error, UI will retry the request (this time it will be fine...)
            # As request will close the image file, we've got to open it again
            with open(file, 'rb') as image:
                fixture_problems_with_storage.side_effect = None
                response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
                    'image': (image, 'slice_1.dcm'),
                }, headers=get_headers(token=user_token, multipart=True))
                assert response.status_code == 201

    # Step 4. Check number of Slices in the databases
    z_slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    assert len(z_slices) == 3
