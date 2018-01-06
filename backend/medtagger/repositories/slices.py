"""Module responsible for definition of Slices' Repository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Slice, SliceOrientation, Scan
from medtagger.types import SliceID, ScanID
from medtagger.clients.hbase_client import HBaseClient


class SlicesRepository(object):
    """Repository for Slices."""

    @staticmethod
    def get_slice_by_id(slice_id: SliceID) -> Slice:
        """Fetch Slice from database."""
        with db_session() as session:
            _slice = session.query(Slice).filter(Slice.id == slice_id).one()
        return _slice

    @staticmethod
    def get_slices_by_scan_id(scan_id: ScanID, orientation: SliceOrientation = SliceOrientation.Z) -> List[Slice]:
        """Fetch Slice from database."""
        with db_session() as session:
            query = session.query(Slice)
            query = query.filter(Scan.id == scan_id)
            query = query.filter(Slice.orientation == orientation)
            slices = query.all()
        return slices

    @staticmethod
    def get_slice_original_image(slice_id: SliceID) -> bytes:
        """Return original Dicom image as bytes."""
        hbase_client = HBaseClient()
        data = hbase_client.get(HBaseClient.ORIGINAL_SLICES_TABLE, slice_id, columns=['image'])
        return data[b'image:value']

    @staticmethod
    def get_slice_converted_image(slice_id: SliceID) -> bytes:
        """Return converted image as bytes."""
        hbase_client = HBaseClient()
        data = hbase_client.get(HBaseClient.CONVERTED_SLICES_TABLE, slice_id, columns=['image'])
        return data[b'image:value']

    @staticmethod
    def store_original_image(slice_id: SliceID, image: bytes) -> None:
        """Store original image into HBase."""
        slice_value = {
            'image:value': image,
        }
        hbase_client = HBaseClient()
        hbase_client.put(HBaseClient.ORIGINAL_SLICES_TABLE, slice_id, slice_value)

    @staticmethod
    def store_converted_image(slice_id: SliceID, image: bytes) -> None:
        """Store converted image into HBase."""
        slice_value = {
            'image:value': image,
        }
        hbase_client = HBaseClient()
        hbase_client.put(HBaseClient.CONVERTED_SLICES_TABLE, slice_id, slice_value)
