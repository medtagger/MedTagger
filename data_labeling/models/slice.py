"""Module responsible for definition of Slice model"""
from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.types import SliceID, SliceLocation, SlicePosition


class Slice(object):
    """Definition of a Slice"""

    def __init__(self, slice_id: SliceID, location: SliceLocation = None, position: SlicePosition = None) -> None:
        """Slice initialization

        :param slice_id: ID of a Slice
        :param location: location where Slice is placed (used for sorting)
        :param position: position for this Slice
        """
        self.id = slice_id
        self.location = location
        self.position = position
        self.hbase_client = HBaseClient()

    @property
    def original_image(self) -> bytes:
        """Return original Dicom image as bytes"""
        data = self.hbase_client.get(HBaseClient.ORIGINAL_SLICES_TABLE, self.id, columns=['image'])
        return data[b'image:value']

    @property
    def converted_image(self) -> bytes:
        """Return converted image as bytes"""
        data = self.hbase_client.get(HBaseClient.CONVERTED_SLICES_TABLE, self.id, columns=['image'])
        return data[b'image:value']
