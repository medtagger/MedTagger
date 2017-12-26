"""Module responsible for asynchronous data conversion."""
import io
import numpy as np

import dicom
from PIL import Image
from scipy import ndimage

from medtagger.types import ScanID
from medtagger.workers import celery_app
from medtagger.conversion import convert_to_normalized_8bit_array
from medtagger.database.models import SliceOrientation, Slice
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.slices import SlicesRepository


@celery_app.task
def convert_scan_to_png(scan_id: ScanID) -> None:
    """Store Scan in HBase database.

    :param scan_id: ID of a Scan
    """
    # At first, collect all Dicom images for given Scan and correlate them with Slices
    all_dicom_images = []
    slices = SlicesRepository.get_slices_by_scan_id(scan_id)
    for _slice in slices:
        image = SlicesRepository.get_slice_original_image(_slice.id)
        image_bytes = io.BytesIO(image)
        dicom_image = dicom.read_file(image_bytes, force=True)
        all_dicom_images.append(dicom_image)

    # Convert all Slices in Z orientation (these were created previously during upload)
    for dicom_image, _slice in zip(all_dicom_images, slices):
        slice_pixels = convert_to_normalized_8bit_array(dicom_image)
        _convert_and_store(_slice, slice_pixels)

    # Now, let's sort all Dicoms with their locations and scale it down to be smaller
    all_dicom_images = sorted(all_dicom_images, key=lambda _slice: _slice.SliceLocation)
    raw_scan = np.array(convert_to_normalized_8bit_array(_slice) for _slice in all_dicom_images)
    raw_scan = np.array(ndimage.zoom(raw_scan, 0.5))  # Scale all images down by a factor of 2
    scan = ScansRepository.get_scan_by_id(scan_id)

    # Prepare Slices in the X orientation
    for i in range(raw_scan.shape[0]):  # TODO: Fix iteration!
        slice_pixels = raw_scan[i, :, :]
        _slice = scan.add_slice(SliceOrientation.X)
        _convert_and_store(_slice, slice_pixels)

    # Prepare Slices in the Y orientation
    for i in range(raw_scan.shape[1]):  # TODO: Fix iteration!
        slice_pixels = raw_scan[:, i, :]
        _slice = scan.add_slice(SliceOrientation.Y)
        _convert_and_store(_slice, slice_pixels)


def _convert_and_store(_slice: Slice, slice_pixels: np.ndarray) -> None:
    """

    :param _slice:
    :param slice_pixels:
    :return:
    """
    converted_image = _convert_slice_pixels(slice_pixels)
    SlicesRepository.store_converted_image(_slice.id, converted_image)
    _slice.mark_as_converted()
    print('{} converted and stored.'.format(_slice))


def _convert_slice_pixels(slice_pixels: np.ndarray) -> bytes:
    """

    :param slice_pixels:
    :return:
    """
    png_image = io.BytesIO()
    Image.fromarray(slice_pixels, 'L').save(png_image, 'PNG')
    png_image.seek(0)
    return png_image.getvalue()
