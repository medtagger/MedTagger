"""Module responsible for definition of SlicesRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Slice, SliceOrientation, Scan
from medtagger.storage.models import OriginalSlice, ProcessedSlice
from medtagger.types import SliceID, ScanID


def get_slice_by_id(slice_id: SliceID) -> Slice:
    """Fetch Slice from database."""
    with db_session() as session:
        _slice = session.query(Slice).filter(Slice.id == slice_id).one()
    return _slice


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


def delete_slice(_slice: Slice) -> None:
    """Remove Slice from SQL database and Storage."""
    delete_slice_by_id(_slice.id, _slice.scan_id)


def delete_slice_by_id(slice_id: SliceID, scan_id: ScanID) -> None:
    """Remove Slice from SQL database and Storage based on IDs."""
    with db_session() as session:
        query = session.query(Scan).filter(Scan.id == scan_id)
        query.update({'declared_number_of_slices': Scan.declared_number_of_slices - 1})
        session.query(Slice).filter(Slice.id == slice_id).delete()

    OriginalSlice.filter(id=slice_id).delete()
    ProcessedSlice.filter(id=slice_id).delete()


def get_slice_original_image(slice_id: SliceID) -> bytes:
    """Return original Dicom image as bytes."""
    original_slice = OriginalSlice.get(id=slice_id)
    return original_slice.image


def get_slice_converted_image(slice_id: SliceID) -> bytes:
    """Return converted image as bytes."""
    original_slice = ProcessedSlice.get(id=slice_id)
    return original_slice.image


def store_original_image(slice_id: SliceID, image: bytes) -> None:
    """Store original image into Storage."""
    OriginalSlice.create(id=slice_id, image=image)


def store_converted_image(slice_id: SliceID, image: bytes) -> None:
    """Store converted image into Storage."""
    ProcessedSlice.create(id=slice_id, image=image)
