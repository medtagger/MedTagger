"""Tests for Scan upload to the system."""
import io
import glob
import json
from typing import Any

from PIL import Image

from medtagger.database.models import SliceOrientation
from medtagger.repositories.slices import SlicesRepository

from tests.functional_tests import get_api_client


# pylint: disable=too-many-locals
def test_scan_upload_and_conversion(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application for Scan upload and conversion."""
    api_client = get_api_client()

    # Step 1. Add Scan to the system
    payload = {'category': 'LUNGS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload), headers={'content-type': 'application/json'})
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 2. Send Slices
    for file in glob.glob('example_data/example_scan/*.dcm'):
        with open(file, 'rb') as image:
            response = api_client.post('/api/v1/scans/{}/slices'.format(scan_id), data={
                'image': (image, 'slice_1.dcm'),
            }, content_type='multipart/form-data')
            assert response.status_code == 201

    # Step 3. Check Scan & Slices in the databases
    z_slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    assert len(z_slices) == 3
    y_slices = SlicesRepository.get_slices_by_scan_id(scan_id, SliceOrientation.Y)
    assert len(y_slices) == 256
    x_slices = SlicesRepository.get_slices_by_scan_id(scan_id, SliceOrientation.X)
    assert len(x_slices) == 256

    # Step 3.1. Slices in Z axis
    z_slice = SlicesRepository.get_slice_converted_image(z_slices[2].id)
    z_slice_image = Image.open(io.BytesIO(z_slice))
    assert z_slice_image.size == (512, 512)

    # Step 3.2. Slices in Y axis
    y_slice = SlicesRepository.get_slice_converted_image(y_slices[128].id)
    y_slice_image = Image.open(io.BytesIO(y_slice))
    assert y_slice_image.size == (256, 186)

    # Step 3.3. Slices in Z axis
    x_slice = SlicesRepository.get_slice_converted_image(x_slices[128].id)
    x_slice_image = Image.open(io.BytesIO(x_slice))
    assert x_slice_image.size == (256, 186)
