"""Module responsible for asynchronous data storage."""
import os
from tempfile import NamedTemporaryFile

import SimpleITK as sitk
from celery.utils.log import get_task_logger

from medtagger.definitions import DicomTags, SliceStatus
from medtagger.types import ScanID, SliceID, SlicePosition, SliceLocation
from medtagger.workers import celery_app
from medtagger.workers.conversion import convert_scan_to_png
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.slices import SlicesRepository

logger = get_task_logger(__name__)


@celery_app.task
def parse_dicom_and_update_slice(slice_id: SliceID) -> None:
    """Parse DICOM from Storage and update Slice for location and position.

    :param slice_id: ID of a slice
    """
    logger.debug('Parsing DICOM file from Storage for given Slice ID: %s.', slice_id)
    _slice = SlicesRepository.get_slice_by_id(slice_id)
    image = SlicesRepository.get_slice_original_image(_slice.id)

    # We've got to store above DICOM image bytes on disk due to the fact that SimpleITK does not support
    # reading files from memory. It has to work on a file stored on a hard drive.
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.write(image)
    temp_file.close()

    try:
        reader = sitk.ImageFileReader()
        reader.SetFileName(temp_file.name)
        reader.ReadImageInformation()

        location = SliceLocation(float(reader.GetMetaData(DicomTags.SLICE_LOCATION.value)))
        image_position_patient = reader.GetMetaData(DicomTags.IMAGE_POSITION_PATIENT.value).split('\\')
        position = SlicePosition(float(image_position_patient[0]),
                                 float(image_position_patient[1]),
                                 float(image_position_patient[2]))
        height = int(reader.GetMetaData(DicomTags.ROWS.value))
        width = int(reader.GetMetaData(DicomTags.COLUMNS.value))

    except RuntimeError:
        logger.error('User sent a file that is not a DICOM.')
        SlicesRepository.delete_slice_by_id(_slice.id)
        ScansRepository.reduce_number_of_declared_slices(_slice.scan_id)
        os.unlink(temp_file.name)
        trigger_scan_conversion_if_needed(_slice.scan_id)
        return

    # Remove temporary file
    os.unlink(temp_file.name)

    _slice.update_location(location)
    _slice.update_position(position)
    _slice.update_size(height, width)
    _slice.update_status(SliceStatus.STORED)
    logger.info('"%s" updated.', _slice)

    trigger_scan_conversion_if_needed(_slice.scan_id)


def trigger_scan_conversion_if_needed(scan_id: ScanID) -> None:
    """Mark Scan as STORED and trigger conversion to PNG if this is the latest uploaded Slice."""
    if ScansRepository.try_to_mark_scan_as_stored(scan_id):
        logger.debug('All Slices uploaded for Scan ID=%s! Running conversion...', scan_id)
        convert_scan_to_png.delay(scan_id)
