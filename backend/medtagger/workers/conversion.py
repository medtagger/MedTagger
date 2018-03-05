"""Module responsible for asynchronous data conversion."""
import io
import os
import tempfile
import numpy as np

import pydicom
from PIL import Image
from celery.utils.log import get_task_logger

from medtagger.types import ScanID
from medtagger.workers import celery_app
from medtagger.conversion import convert_slice_to_normalized_8bit_array, convert_scan_to_normalized_8bit_array
from medtagger.database.models import SliceOrientation, Slice, Scan
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.slices import SlicesRepository

logger = get_task_logger(__name__)

MAX_PREVIEW_X_SIZE = 256


@celery_app.task
def convert_scan_to_png(scan_id: ScanID) -> None:
    """Store Scan in HBase database.

    :param scan_id: ID of a Scan
    """
    logger.info('Starting Scan (%s) conversion.', scan_id)
    temp_files_to_remove = []
    scan = ScansRepository.get_scan_by_id(scan_id)
    slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    if scan.declared_number_of_slices == 0:
        logger.error('This Scan is empty! Removing from database...')
        ScansRepository.delete_scan_by_id(scan_id)
        return

    # At first, collect all Dicom images for given Scan
    logger.info('Reading all Slices for this Scan.')
    dicom_images = []
    for _slice in slices:
        image = SlicesRepository.get_slice_original_image(_slice.id)
        # UGLY WORKAROUND - Start
        temp_file_name = _create_temporary_file(image)
        temp_files_to_remove.append(temp_file_name)
        # UGLY WORKAROUND - Stop
        dicom_image = pydicom.read_file(temp_file_name, force=True)
        dicom_images.append(dicom_image)

    # Correlate Dicom files with Slices and convert all Slices in the Z axis orientation
    logger.info('Converting each Slice in Z axis.')
    for dicom_image, _slice in zip(dicom_images, slices):
        slice_pixels = convert_slice_to_normalized_8bit_array(dicom_image)
        _convert_to_png_and_store(_slice, slice_pixels)

    # Prepare a preview size and convert 3D scan to fit its max X's axis shape
    logger.info('Normalizing Scan in 3D. This may take a while...')
    normalized_scan = convert_scan_to_normalized_8bit_array(dicom_images, output_x_size=MAX_PREVIEW_X_SIZE)

    # Prepare Slices in other orientations
    logger.info('Preparing Slices in other axis.')
    _prepare_slices_in_y_orientation(normalized_scan, scan)
    _prepare_slices_in_x_orientation(normalized_scan, scan)

    logger.info('Marking whole Scan as converted.')
    scan.mark_as_converted()

    # Remove all temporarily created files for applying workaround
    for file_name in temp_files_to_remove:
        os.remove(file_name)


def _create_temporary_file(image: bytes) -> str:
    """Create new temporary file based on given DICOM image.

    This workaround enable support for compressed DICOMs that will be read by the GDCM
    low-level library. Please remove this workaround as soon as this FIX ME notice
    will be removed:
       https://github.com/pydicom/pydicom/blob/master/pydicom/pixel_data_handlers/gdcm_handler.py#L77
    and this Issue will be closed:
       https://github.com/pydicom/pydicom/issues/233

    :param image: bytes with DICOM image
    :return: path to temporary file
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_name = temp_file.name
        temp_file.write(image)
    return temp_file_name


def _prepare_slices_in_y_orientation(normalized_scan: np.ndarray, scan: Scan) -> None:
    """Prepare and save Slices in Y orientation.

    :param normalized_scan: Numpy array with 3D normalized Scan
    :param scan: Scan object to which new Slices should be added
    """
    for y in range(normalized_scan.shape[1]):
        location = 100.0 * y / normalized_scan.shape[1]
        slice_pixels = normalized_scan[:, y, :]
        _slice = scan.add_slice(SliceOrientation.Y)
        _slice.update_location(location)
        _convert_to_png_and_store(_slice, slice_pixels)


def _prepare_slices_in_x_orientation(normalized_scan: np.ndarray, scan: Scan) -> None:
    """Prepare and save Slices in Y orientation.

    :param normalized_scan: Numpy array with 3D normalized Scan
    :param scan: Scan object to which new Slices should be added
    """
    for x in range(normalized_scan.shape[2]):
        location = 100.0 * x / normalized_scan.shape[2]
        slice_pixels = normalized_scan[:, :, x]
        _slice = scan.add_slice(SliceOrientation.X)
        _slice.update_location(location)
        _convert_to_png_and_store(_slice, slice_pixels)


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
