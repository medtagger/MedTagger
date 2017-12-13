"""Module responsible for definition of Slices' Repository"""
from data_labeling.database import db_session
from data_labeling.database.models import Slice
from data_labeling.types import SliceID
from data_labeling.clients.hbase_client import HBaseClient


class SlicesRepository(object):
    """Repository for Slices"""

    @staticmethod
    def get_slice_by_id(slice_id: SliceID) -> Slice:
        """Fetch Slice from database"""
        with db_session() as session:
            _slice = session.query(Slice).filter(Slice.id == slice_id).one()
        return _slice

    @staticmethod
    def get_slice_original_image(slice_id: SliceID) -> bytes:
        """Return original Dicom image as bytes"""
        hbase_client = HBaseClient()
        data = hbase_client.get(HBaseClient.ORIGINAL_SLICES_TABLE, slice_id, columns=['image'])
        return data[b'image:value']

    @staticmethod
    def get_slice_converted_image(slice_id: SliceID) -> bytes:
        """Return converted image as bytes"""
        hbase_client = HBaseClient()
        data = hbase_client.get(HBaseClient.CONVERTED_SLICES_TABLE, slice_id, columns=['image'])
        return data[b'image:value']

    @staticmethod
    def store_original_image(slice_id: SliceID, image: bytes) -> None:
        """Store original image into HBase"""
        slice_value = {
            'image:value': image,
        }
        hbase_client = HBaseClient()
        hbase_client.put(HBaseClient.ORIGINAL_SLICES_TABLE, slice_id, slice_value)

    @staticmethod
    def store_converted_image(slice_id: SliceID, image: bytes) -> None:
        """Store converted image into HBase"""
        slice_value = {
            'image:value': image,
        }
        hbase_client = HBaseClient()
        hbase_client.put(HBaseClient.CONVERTED_SLICES_TABLE, slice_id, slice_value)
