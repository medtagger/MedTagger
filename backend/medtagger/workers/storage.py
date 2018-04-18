"""Module responsible for asynchronous data storage."""
import os
from tempfile import NamedTemporaryFile

import SimpleITK as sitk
from celery.utils.log import get_task_logger

from medtagger.types import ScanID, SliceID, SlicePosition, SliceLocation
from medtagger.workers import celery_app
from medtagger.workers.conversion import convert_scan_to_png
from medtagger.repositories.scans import ScansRepository
from medtagger.repositories.slices import SlicesRepository

logger = get_task_logger(__name__)

SLICE_LOCATION_TAG = '0020|1041'
IMAGE_POSITION_PATIENT_TAG = '0020|0032'


@celery_app.task
def parse_dicom_and_update_slice(slice_id: SliceID) -> None:
    """Parse Dicom from HBase and update Slice for location and position.

    :param slice_id: ID of a slice
    """
    logger.debug('Parsing Dicom file from HBase for given Slice ID: %s.', slice_id)
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

        location = SliceLocation(float(reader.GetMetaData(SLICE_LOCATION_TAG)))
        image_position_patient = reader.GetMetaData(IMAGE_POSITION_PATIENT_TAG).split('\\')
        position = SlicePosition(float(image_position_patient[0]),
                                 float(image_position_patient[1]),
                                 float(image_position_patient[2]))
    except RuntimeError:
        logger.error('User sent a file that is not a DICOM.')
        SlicesRepository.delete_slice_by_id(_slice.id)
        ScansRepository.reduce_number_of_declared_slices(_slice.scan_id)
        trigger_scan_conversion_if_needed(_slice.scan_id)
        return

    # Remove temporary file
    os.unlink(temp_file.name)

    _slice.update_location(location)
    _slice.update_position(position)
    _slice.mark_as_stored()
    logger.info('"%s" updated.', _slice)

    # Run conversion to PNG if this is the latest uploaded Slice
    trigger_scan_conversion_if_needed(_slice.scan_id)


def trigger_scan_conversion_if_needed(scan_id: ScanID) -> None:
    """Run conversion if all Slices for given Scan were uploaded."""
    scan = ScansRepository.get_scan_by_id(scan_id)
    logger.debug('Stored %s Slices. Waiting for %s Slices.', len(scan.stored_slices), scan.declared_number_of_slices)
    if scan.declared_number_of_slices == len(scan.stored_slices):
        logger.debug('All Slices uploaded for %s! Running conversion...', scan)
        convert_scan_to_png.delay(scan.id)
