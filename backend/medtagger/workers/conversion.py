"""Module responsible for asynchronous data conversion."""
import io
import logging
import numpy as np

import dicom
from PIL import Image

from medtagger.types import ScanID
from medtagger.workers import celery_app
from medtagger.conversion import convert_slice_to_normalized_8bit_array, convert_scan_to_normalized_8bit_array
from medtagger.database.models import SliceOrientation, Slice
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.slices import SlicesRepository

logger = logging.getLogger(__name__)


@celery_app.task
def convert_scan_to_png(scan_id: ScanID) -> None:
    """Store Scan in HBase database.

    :param scan_id: ID of a Scan
    """
    scan = ScansRepository.get_scan_by_id(scan_id)
    slices = SlicesRepository.get_slices_by_scan_id(scan_id)

    # At first, collect all Dicom images for given Scan
    dicom_images = []
    for _slice in slices:
        image = SlicesRepository.get_slice_original_image(_slice.id)
        image_bytes = io.BytesIO(image)
        dicom_image = dicom.read_file(image_bytes, force=True)
        dicom_images.append(dicom_image)

    # Correlate Dicom files with Slices and convert all Slices in the Z axis orientation
    for dicom_image, _slice in zip(dicom_images, slices):
        slice_pixels = convert_slice_to_normalized_8bit_array(dicom_image)
        _convert_to_png_and_store(_slice, slice_pixels)

    # Prepare a preview size and convert 3D scan to fit its max X's axis shape
    max_preview_x_size = 256
    normalized_scan = convert_scan_to_normalized_8bit_array(dicom_images, output_x_size=max_preview_x_size)

    # Prepare Slices in the Y orientation
    for y in range(normalized_scan.shape[1]):
        location = 100.0 * y / normalized_scan.shape[1]
        slice_pixels = normalized_scan[:, y, :]
        _slice = scan.add_slice(SliceOrientation.Y)
        _slice.update_location(location)
        _convert_to_png_and_store(_slice, slice_pixels)

    # Prepare Slices in the X orientation
    for x in range(normalized_scan.shape[2]):
        location = 100.0 * x / normalized_scan.shape[2]
        slice_pixels = normalized_scan[:, :, x]
        _slice = scan.add_slice(SliceOrientation.X)
        _slice.update_location(location)
        _convert_to_png_and_store(_slice, slice_pixels)

    logger.info('Marking whole Scan as converted.')
    scan.mark_as_converted()


def _convert_to_png_and_store(_slice: Slice, slice_pixels: np.ndarray) -> None:
    """Convert given Slice's pixel array and store in databases.

    :param _slice: Slice database object
    :param slice_pixels: numpy array with Slice data
    """
    converted_image = _convert_slice_pixels_to_png(slice_pixels)
    SlicesRepository.store_converted_image(_slice.id, converted_image)
    _slice.mark_as_converted()
    logger.info('%s converted and stored.', _slice)


def _convert_slice_pixels_to_png(slice_pixels: np.ndarray) -> bytes:
    """Convert given Slice's pixel array to the PNG format in bytes.

    :param slice_pixels: Slice's pixel array
    :return: bytes with Slice formatted in PNG
    """
    png_image = io.BytesIO()
    Image.fromarray(slice_pixels, 'L').save(png_image, 'PNG')
    png_image.seek(0)
    return png_image.getvalue()
