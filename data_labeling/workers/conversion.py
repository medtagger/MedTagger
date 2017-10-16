"""Module responsible for asynchronous data conversion"""
import pickle
from typing import cast

from dicom.dataset import FileDataset
from PIL import Image

from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.types import ScanID, SliceID, PickledDicomImage
from data_labeling.workers import celery_app
from data_labeling.conversion import convert_to_normalized_8bit_array
from data_labeling.workers.helpers import prepare_hbase_slice_entry


@celery_app.task
def convert_dicom_to_png(scan_id: ScanID, slice_id: SliceID, dicom_image: FileDataset) -> None:
    """Store Dicom in HBase database

     Key is a combination of a ScanID followed by unique SliceID. It also fetch from Dicom information about
     patient position together with slice location that might be helpful while sorting and fetching slices
     for given ScanID.

    :param scan_id: ID of a scan that contains given slice
    :param slice_id: ID of a slice
    :param dicom_image: Dicom object

    Converted dicoms file are then saved to Hbase
    """
    pixel_array = convert_to_normalized_8bit_array(dicom_image)
    pickled_dicom_image = cast(PickledDicomImage, pickle.dumps(Image.fromarray(pixel_array).tobytes()))

    slice_key, slice_value = prepare_hbase_slice_entry(scan_id, slice_id, dicom_image)
    slice_value['image:value'] = pickled_dicom_image

    connection = HBaseClient()
    slices_table = connection.table(HBaseClient.CONVERTED_SLICES_TABLE)
    slices_table.put(slice_key, slice_value)
    print('Converted slice stored under "{}".'.format(slice_key))
