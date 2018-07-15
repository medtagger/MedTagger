"""Module responsible for definition of Slices' Repository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Slice, SliceOrientation, Scan
from medtagger.storage.models import OriginalSlice, ProcessedSlice
from medtagger.types import SliceID, ScanID


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
            query = query.join(Scan)
            query = query.filter(Scan.id == scan_id)
            query = query.filter(Slice.orientation == orientation)
            query = query.order_by(Slice.location)
            slices = query.all()
        return slices

    @staticmethod
    def delete_slice_by_id(slice_id: SliceID) -> None:
        """Remove Slice from SQL database and Storage."""
        with db_session() as session:
            session.query(Slice).filter(Slice.id == slice_id).delete()
        OriginalSlice.filter(id=slice_id).delete()
        ProcessedSlice.filter(id=slice_id).delete()

    @staticmethod
    def get_slice_original_image(slice_id: SliceID) -> bytes:
        """Return original Dicom image as bytes."""
        original_slice = OriginalSlice.get(id=slice_id)
        return original_slice.image

    @staticmethod
    def get_slice_converted_image(slice_id: SliceID) -> bytes:
        """Return converted image as bytes."""
        original_slice = ProcessedSlice.get(id=slice_id)
        return original_slice.image

    @staticmethod
    def store_original_image(slice_id: SliceID, image: bytes) -> None:
        """Store original image into Storage."""
        OriginalSlice.create(id=slice_id, image=image)

    @staticmethod
    def store_converted_image(slice_id: SliceID, image: bytes) -> None:
        """Store converted image into Storage."""
        ProcessedSlice.create(id=slice_id, image=image)
