"""Module responsible for definition of SlicesRepository."""
from typing import List, Set

from medtagger import definitions
from medtagger.database import db_connection_session, db_transaction_session, models as db_models
from medtagger.storage.models import OriginalSlice, ProcessedSlice
from medtagger.types import SliceID, ScanID


def get_slice_by_id(slice_id: SliceID) -> db_models.Slice:
    """Fetch Slice from database."""
    with db_connection_session() as session:
        return session.query(db_models.Slice).filter(db_models.Slice.id == slice_id).one()


def get_slices_by_scan_id(scan_id: ScanID, orientation: definitions.SliceOrientation = definitions.SliceOrientation.Z) \
        -> List[db_models.Slice]:
    """Fetch Slice from database."""
    with db_connection_session() as session:
        query = session.query(db_models.Slice)
        query = query.join(db_models.Scan)
        query = query.filter(db_models.Scan.id == scan_id)
        query = query.filter(db_models.Slice.orientation == orientation)
        query = query.order_by(db_models.Slice.location)
        slices = query.all()
    return slices


def get_slices_ids_for_labeled_scans(label_elements: List[db_models.LabelElement]) -> Set[SliceID]:
    """Fetch Slices' IDs for all Scans that were labeled within given Label Elements.

    :param label_elements: list of Label Elements objects
    :return: set of all Slice IDs
    """
    scans_ids = {label_element.label.scan_id for label_element in label_elements}
    with db_connection_session() as session:
        query = session.query(db_models.Slice).with_entities(db_models.Slice.id)
        query = query.filter(db_models.Slice.scan_id.in_(scans_ids))  # type: ignore  # "ScanID" has no attribute "in_"
        slices = query.all()
    return {_slice.id for _slice in slices}


def delete_slice(_slice: db_models.Slice) -> None:
    """Remove Slice from SQL database and Storage."""
    slice_id = _slice.id
    scan_id = _slice.scan_id

    with db_transaction_session() as session:
        query = session.query(db_models.Scan).filter(db_models.Scan.id == scan_id)
        query.update({'declared_number_of_slices': db_models.Scan.declared_number_of_slices - 1})
        session.query(db_models.Slice).filter(db_models.Slice.id == slice_id).delete()

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
