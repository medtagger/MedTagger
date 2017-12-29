"""Tests for Scan upload to the system."""
import io
import os
import json
from typing import Any

from PIL import Image
import numpy as np

from medtagger.database.models import SliceOrientation
from medtagger.repositories.slices import SlicesRepository

from tests.functional_tests import get_api_client, get_web_socket_client


def test_scan_upload_and_conversion(prepare_environment: Any, synchronous_celery: Any) -> None:
    """Test application for Scan upload and conversion."""
    api_client = get_api_client()
    web_socket_client = get_web_socket_client(namespace='/slices')

    # Step 1. Add Scan to the system
    payload = {'category': 'LUNGS', 'number_of_slices': 3}
    response = api_client.post('/api/v1/scans/', data=json.dumps(payload), headers={'content-type': 'application/json'})
    json_response = json.loads(response.data)
    scan_id = json_response['scan_id']

    # Step 2. Send Slices through Web Socket
    for filename in os.listdir('example_data/example_scan/'):
        with open('example_data/example_scan/' + filename, 'rb') as image:
            binary_image = image.read()
            web_socket_client.emit('upload_slice', {'scan_id': scan_id, 'image': binary_image}, namespace='/slices')

    # Step 3. Check Scan & Slices in the databases
    z_slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    assert len(z_slices) == 3
    y_slices = SlicesRepository.get_slices_by_scan_id(scan_id, SliceOrientation.Y)
    assert len(y_slices) == 256
    x_slices = SlicesRepository.get_slices_by_scan_id(scan_id, SliceOrientation.X)
    assert len(x_slices) == 256

    # Step 3.1. Slices in Z axis
    z_slice = SlicesRepository.get_slice_converted_image(z_slices[1].id)
    z_slice_image = Image.open(io.BytesIO(z_slice))
    assert np.sum(np.asarray(z_slice_image)) == 33552903  # Difference means that algorithm has changed
    assert z_slice_image.size == (512, 512)

    # Step 3.2. Slices in Y axis
    y_slice = SlicesRepository.get_slice_converted_image(y_slices[128].id)
    y_slice_image = Image.open(io.BytesIO(y_slice))
    assert np.sum(np.asarray(y_slice_image)) == 6800579  # Difference means that algorithm has changed
    assert y_slice_image.size == (256, 186)

    # Step 3.3. Slices in Z axis
    x_slice = SlicesRepository.get_slice_converted_image(x_slices[128].id)
    x_slice_image = Image.open(io.BytesIO(x_slice))
    assert np.sum(np.asarray(x_slice_image)) == 6167896  # Difference means that algorithm has changed
    assert x_slice_image.size == (256, 186)
