"""Module responsible for definition of ScansRepository."""
from typing import List, Tuple

from sqlalchemy.sql.expression import func

from medtagger.database import db_connection_session, db_transaction_session
from medtagger.database.models import Dataset, Scan, Slice, User, Label, Task, datasets_tasks
from medtagger.definitions import ScanStatus, SliceStatus
from medtagger.types import ScanID


def get_paginated_scans(dataset_key: str = None, page: int = 1, per_page: int = 25) -> Tuple[List[Scan], int]:
    """Fetch and return all Scans filtered by given parameters.

    :param dataset_key: (optional) key for Dataset that should be used as a filter
    :param page: (optional) page number which should be fetched
    :param per_page: (optional) number of entries per page
    :return: tuple of list of Scans and total number of entries available
    """
    query = Scan.query
    if dataset_key:
        query = query.join(Dataset)
        query = query.filter(Dataset.key == dataset_key)
    query = query.order_by(Scan.id)

    scans = query.limit(per_page).offset((page - 1) * per_page).all()
    total_scans = query.count()
    return scans, total_scans


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
        labeled_scans_ids = Label.query.with_entities(Label.scan_id)
        labeled_scans_ids = labeled_scans_ids.filter(Label.owner == user)
        if task:
            labeled_scans_ids = labeled_scans_ids.filter(Label.task == task)
            labeled_scans_ids = labeled_scans_ids.filter(~Label.is_predefined)
        query = query.filter(~Scan.id.in_(labeled_scans_ids.subquery()))  # type: ignore  # "ScanID" doesn't have "in_"
    query = query.filter(Scan.status == ScanStatus.AVAILABLE)
    query = query.order_by(func.random())
    return query.first()


def delete_scan_by_id(scan_id: ScanID) -> None:
    """Remove Scan from SQL database."""
    with db_connection_session() as session:
        scan = session.query(Scan).filter(Scan.id == scan_id).one()
    with db_transaction_session() as session:
        session.delete(scan)


def add_new_scan(dataset: Dataset, number_of_slices: int, user: User = None) -> Scan:
    """Add new Scan to the database.

    :param dataset: Dataset object
    :param number_of_slices: number of Slices that will be uploaded
    :param user: (optional) User that uploaded scan
    :return: Scan object
    """
    scan = Scan(dataset, number_of_slices, user)
    with db_transaction_session() as session:
        session.add(scan)
    return scan


def try_to_mark_scan_as_stored(scan_id: ScanID) -> bool:
    """Mark Scan as STORED only if all Slices were STORED.

    :param scan_id: ID of a Scan which should be tried to mark as STORED
    :return: boolean information if Scan was marked or not
    """
    with db_transaction_session() as session:
        stored_slices_subquery = session.query(func.count(Slice.id).label('count'))
        stored_slices_subquery = stored_slices_subquery.filter(Slice.scan_id == scan_id)
        stored_slices_subquery = stored_slices_subquery.filter(Slice.status == SliceStatus.STORED)
        stored_slices_subquery = stored_slices_subquery.subquery()

        query = session.query(Scan)
        query = query.filter(Scan.id == scan_id)
        query = query.filter(Scan.status != ScanStatus.STORED)
        query = query.filter(Scan.declared_number_of_slices == stored_slices_subquery.c.count)
        updated = query.update({'status': ScanStatus.STORED}, synchronize_session=False)
        return bool(updated)


def increase_skip_count_of_a_scan(scan_id: ScanID) -> bool:
    """Increase skip_count of a Scan with given scan_id.

    :param scan_id: ID of a Scan which skip_count should be increased
    :return: boolean information whether the Scan was skipped or not
    """
    with db_transaction_session() as session:
        query = session.query(Scan)
        query = query.filter(Scan.id == scan_id)
        updated = query.update({'skip_count': Scan.skip_count + 1})
        return bool(updated)
