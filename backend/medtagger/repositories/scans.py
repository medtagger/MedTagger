"""Module responsible for definition of ScansRepository."""
from typing import Optional, List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import Dataset, Scan, Slice, User, Label, Task, datasets_tasks
from medtagger.definitions import ScanStatus, SliceStatus
from medtagger.types import ScanID


def get_all_scans() -> List[Scan]:
    """Fetch all Scans from database."""
    return Scan.query.all()


def get_scan_by_id(scan_id: ScanID) -> Scan:
    """Fetch Scan from database."""
    return Scan.query.filter(Scan.id == scan_id).one()


def get_random_scan(task: Task = None, user: User = None) -> Scan:
    """Fetch random Scan from database.

    :param task: (optional) Task from which scan should be fetched
    :param user: (optional) User for which Scan should be randomized
    :return: Label object
    """
    query = Scan.query
    if task:
        query = query.join(Dataset).join(datasets_tasks).join(Task)
        query = query.filter(Task.key == task.key)
    if user:
        labelled_scans = Label.query.filter(Label.owner == user).all()
        labelled_scans_ids = [label.scan_id for label in labelled_scans]
        query = query.filter(~Scan.id.in_(labelled_scans_ids))  # type: ignore  # "ScanID" has no attribute "in_"
    query = query.filter(Scan.status == ScanStatus.AVAILABLE)
    query = query.order_by(func.random())
    return query.first()


def delete_scan_by_id(scan_id: ScanID) -> None:
    """Remove Scan from SQL database."""
    with db_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
        session.delete(scan)


def add_new_scan(dataset: Dataset, number_of_slices: int, user: Optional[User]) -> Scan:
    """Add new Scan to the database.

    :param dataset: Dataset object
    :param number_of_slices: number of Slices that will be uploaded
    :param user: User that uploaded scan
    :return: Scan object
    """
    with db_session() as session:
        scan = Scan(dataset, number_of_slices, user)
        session.add(scan)
    return scan


def try_to_mark_scan_as_stored(scan_id: ScanID) -> bool:
    """Mark Scan as STORED only if all Slices were STORED.

    :param scan_id: ID of a Scan which should be tried to mark as STORED
    :return: boolean information if Scan was marked or not
    """
    with db_session() as session:
        stored_slices_subquery = session.query(func.count(Slice.id).label('count'))
        stored_slices_subquery = stored_slices_subquery.filter(Slice.scan_id == scan_id)
        stored_slices_subquery = stored_slices_subquery.filter(Slice.status == SliceStatus.STORED)
        stored_slices_subquery = stored_slices_subquery.subquery()

        query = session.query(Scan)
        query = query.filter(Scan.id == scan_id)
        query = query.filter(Scan.status != ScanStatus.STORED)
        query = query.filter(Scan.declared_number_of_slices == stored_slices_subquery.c.count)
        updated = query.update({"status": (ScanStatus.STORED)}, synchronize_session=False)
        return bool(updated)


def increase_skip_count_of_a_scan(scan_id: ScanID) -> bool:
    """Increase skip_count of a Scan with given scan_id.

    :param scan_id: ID of a Scan which skip_count should be increased
    :return: boolean information whether the Scan was skipped or not
    """
    with db_session() as session:
        query = session.query(Scan)
        query = query.filter(Scan.id == scan_id)
        updated = query.update({"skip_count": (Scan.skip_count + 1)})
        return bool(updated)
