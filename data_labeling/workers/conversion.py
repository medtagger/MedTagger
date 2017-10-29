"""Module responsible for asynchronous data conversion"""
from io import BytesIO

from dicom.dataset import FileDataset
from PIL import Image

from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.types import SliceID
from data_labeling.workers import celery_app
from data_labeling.conversion import convert_to_normalized_8bit_array


@celery_app.task
def convert_dicom_to_png(slice_id: SliceID, dicom_image: FileDataset) -> None:
    """Store Dicom in HBase database

    :param slice_id: ID of a slice
    :param dicom_image: Dicom object

    Converted dicoms file are then saved to Hbase
    """
    pixel_array = convert_to_normalized_8bit_array(dicom_image)
    png_image = BytesIO()
    Image.fromarray(pixel_array, 'L').save(png_image, 'PNG')
    png_image.seek(0)

    slice_value = {
        'image:value': png_image.getvalue(),
    }

    hbase_client = HBaseClient()
    hbase_client.put(HBaseClient.CONVERTED_SLICES_TABLE, slice_id, slice_value)
    print('Converted slice stored under "{}".'.format(slice_id))
