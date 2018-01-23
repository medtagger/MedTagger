"""Module responsible for asynchronous data storage."""
import io
import logging

import dicom

from medtagger.types import SliceID, SlicePosition, SliceLocation
from medtagger.workers import celery_app
from medtagger.workers.conversion import convert_scan_to_png
from medtagger.repositories.slices import SlicesRepository

logger = logging.getLogger(__name__)


@celery_app.task
def parse_dicom_and_update_slice(slice_id: SliceID) -> None:
    """Parse Dicom from HBase and update Slice for location and position.

    :param slice_id: ID of a slice
    """
    logger.debug('Parsing Dicom file from HBase for given Slice ID: %s.', slice_id)
    image = SlicesRepository.get_slice_original_image(slice_id)
    image_bytes = io.BytesIO(image)
    dicom_image = dicom.read_file(image_bytes, stop_before_pixels=True, force=True)

    location = SliceLocation(dicom_image.SliceLocation)
    position = SlicePosition(dicom_image.ImagePositionPatient[0],
                             dicom_image.ImagePositionPatient[1],
                             dicom_image.ImagePositionPatient[2])

    _slice = SlicesRepository.get_slice_by_id(slice_id)
    _slice.update_location(location)
    _slice.update_position(position)
    _slice.mark_as_stored()
    logger.info('"%s" updated.', _slice)

    # Run conversion to PNG if this is the latest uploaded Slice
    scan = _slice.scan
    logger.debug('Stored %s Slices. Waiting for %s Slices.', len(scan.stored_slices), scan.declared_number_of_slices)
    if scan.declared_number_of_slices == len(scan.stored_slices):
        logger.debug('All Slices uploaded for %s! Running conversion...', scan)
        convert_scan_to_png.delay(scan.id)
