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
def store_dicom(slice_id: SliceID) -> None:
    """Store Dicom in HBase database.

    Key is a combination of a ScanID followed by unique SliceID. It also fetch from Dicom information about
     patient position together with slice location that might be helpful while sorting and fetching slices
     for given ScanID.

    :param slice_id: ID of a slice
    """
    image = SlicesRepository.get_slice_original_image(slice_id)
    image_bytes = io.BytesIO(image)
    dicom_image = dicom.read_file(image_bytes, force=True)

    location = SliceLocation(dicom_image.SliceLocation)
    position = SlicePosition(dicom_image.ImagePositionPatient[0],
                             dicom_image.ImagePositionPatient[1],
                             dicom_image.ImagePositionPatient[2])

    _slice = SlicesRepository.get_slice_by_id(slice_id)
    _slice.update_location(location)
    _slice.update_position(position)
    _slice.mark_as_stored()
    logger.info('Slice stored under "%s".', slice_id)

    # Run conversion to PNG if this is the latest uploaded Slice
    scan = _slice.scan
    logger.debug('Stored %s Slices. Waiting for %s Slices.', len(scan.slices), scan.number_of_slices)
    # Check if number of declared Slices is the same as number of Slices in DB
    if scan.number_of_slices == len(scan.slices):
        logger.debug('All Slices uploaded for %s! Running conversion...', scan)
        convert_scan_to_png.delay(scan.id)
