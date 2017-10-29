"""Module responsible for asynchronous data storage"""
import pickle
from typing import cast

from dicom.dataset import FileDataset

from data_labeling.types import SliceID, PickledDicomImage
from data_labeling.workers import celery_app
from data_labeling.clients.hbase_client import HBaseClient


@celery_app.task
def store_dicom(slice_id: SliceID, dicom_image: FileDataset) -> None:
    """Store Dicom in HBase database

    Key is a combination of a ScanID followed by unique SliceID. It also fetch from Dicom information about
     patient position together with slice location that might be helpful while sorting and fetching slices
     for given ScanID.

    :param slice_id: ID of a slice
    :param dicom_image: Dicom object
    """
    pickled_dicom_image = cast(PickledDicomImage, pickle.dumps(dicom_image))
    slice_value = {
        'image:value': pickled_dicom_image,
    }

    hbase_client = HBaseClient()
    hbase_client.put(HBaseClient.ORIGINAL_SLICES_TABLE, slice_id, slice_value)
    print('Slice stored under "{}".'.format(slice_id))
