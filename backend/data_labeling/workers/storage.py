"""Module responsible for asynchronous data storage"""
import io
import dicom

from data_labeling.types import SliceID, SlicePosition, SliceLocation
from data_labeling.workers import celery_app
from data_labeling.repositories.slices import SlicesRepository


@celery_app.task
def store_dicom(slice_id: SliceID, image: bytes) -> None:
    """Store Dicom in HBase database

    Key is a combination of a ScanID followed by unique SliceID. It also fetch from Dicom information about
     patient position together with slice location that might be helpful while sorting and fetching slices
     for given ScanID.

    :param slice_id: ID of a slice
    :param image: bytes representing Dicom file
    """
    image_bytes = io.BytesIO(image)
    dicom_image = dicom.read_file(image_bytes, force=True)

    location = SliceLocation(dicom_image.SliceLocation)
    position = SlicePosition(dicom_image.ImagePositionPatient[0],
                             dicom_image.ImagePositionPatient[1],
                             dicom_image.ImagePositionPatient[2])

    _slice = SlicesRepository.get_slice_by_id(slice_id)
    _slice.update_location(location)
    _slice.update_position(position)
    SlicesRepository.store_original_image(slice_id, image)
    _slice.mark_as_stored()
    print('Slice stored under "{}".'.format(slice_id))
