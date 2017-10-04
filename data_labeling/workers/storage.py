"""Module responsible for asynchronous data storage"""
import uuid
import pickle
from typing import cast
from dicom.dataset import FileDataset

from data_labeling.types import ScanID, PickledDicomImage
from data_labeling.workers import celery_app
from data_labeling.clients.hbase_client import HBaseClient


@celery_app.task
def store_dicom(scan_id: ScanID, dicom_image: FileDataset) -> None:
    """Store Dicom in HBase database

    Key is a combination of a ScanID followed by unique SliceID. It also fetch from Dicom information about
     patient position together with slice location that might be helpful while sorting and fetching slices
     for given ScanID.

    :param scan_id: ID of a scan that contains given slice
    :param dicom_image: Dicom object
    """
    position = dicom_image.ImagePositionPatient
    pickled_dicom_image = cast(PickledDicomImage, pickle.dumps(dicom_image))

    slice_id = str(uuid.uuid4())
    slice_key = str(scan_id) + '__' + str(slice_id)
    slice_value = {
        'position:x': str(position[0]),
        'position:y': str(position[1]),
        'position:z': str(position[2]),
        'position:location': str(dicom_image.SliceLocation),
        'image:value': pickled_dicom_image,
    }

    connection = HBaseClient()
    slices_table = connection.table(HBaseClient.ORIGINAL_SLICES_TABLE)
    slices_table.put(slice_key, slice_value)
    print('Slice stored under "{}".'.format(slice_key))
