"""Module responsible for asynchronous data conversion."""
import io

import dicom
from PIL import Image

from data_labeling.types import SliceID
from data_labeling.workers import celery_app
from data_labeling.conversion import convert_to_normalized_8bit_array
from data_labeling.repositories.slices import SlicesRepository


@celery_app.task
def convert_dicom_to_png(slice_id: SliceID, image: bytes) -> None:
    """Store Dicom in HBase database.

    :param slice_id: ID of a slice
    :param image: bytes representing Dicom file
    """
    image_bytes = io.BytesIO(image)
    dicom_image = dicom.read_file(image_bytes, force=True)

    pixel_array = convert_to_normalized_8bit_array(dicom_image)
    png_image = io.BytesIO()
    Image.fromarray(pixel_array, 'L').save(png_image, 'PNG')
    png_image.seek(0)
    image = png_image.getvalue()

    SlicesRepository.store_converted_image(slice_id, image)
    _slice = SlicesRepository.get_slice_by_id(slice_id)
    _slice.mark_as_converted()
    print('Converted slice stored under "{}".'.format(slice_id))
