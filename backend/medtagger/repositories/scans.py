"""Module responsible for definition of Scans' Repository."""
from typing import Optional, List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Scan, Slice, User, Label
from medtagger.definitions import ScanStatus, SliceStatus
from medtagger.types import ScanID


class ScansRepository(object):
    """Repository for Scans."""

    @staticmethod
    def get_all_scans() -> List[Scan]:
        """Fetch all Scans from database."""
        return Scan.query.all()

    @staticmethod
    def get_scan_by_id(scan_id: ScanID) -> Scan:
        """Fetch Scan from database."""
        return Scan.query.filter(Scan.id == scan_id).one()

    @staticmethod
    def get_random_scan(category: ScanCategory = None, user: User = None) -> Scan:
        """Fetch random Scan from database.

        :param category: (optional) Scan's Category object
        :param user: (optional) User for which Scan should be randomized
        :return: Label object
        """
        query = Scan.query
        if category:
            query = query.join(ScanCategory)
            query = query.filter(ScanCategory.key == category.key)
        if user:
            labelled_scans = Label.query.filter(Label.owner == user).all()
            labelled_scans_ids = [label.scan_id for label in labelled_scans]
            query = query.filter(~Scan.id.in_(labelled_scans_ids))  # type: ignore  # "ScanID" has no attribute "in_"
        query = query.filter(Scan.status == ScanStatus.AVAILABLE)
        query = query.order_by(func.random())
        return query.first()

    @staticmethod
    def delete_scan_by_id(scan_id: ScanID) -> None:
        """Remove Scan from SQL database."""
        with db_session() as session:
            session.query(Scan).filter(Scan.id == scan_id).delete()

    @staticmethod
    def add_new_scan(category: ScanCategory, number_of_slices: int, user: Optional[User]) -> Scan:
        """Add new Scan to the database.

        :param category: Scan's Category object
        :param number_of_slices: number of Slices that will be uploaded
        :param user: User that uploaded scan
        :return: Scan object
        """
        with db_session() as session:
            scan = Scan(category, number_of_slices, user)
            session.add(scan)
        return scan

    @staticmethod
    def reduce_number_of_declared_slices(scan_id: ScanID) -> None:
        """Decrease number of declared Slices by one."""
        with db_session() as session:
            query = session.query(Scan)
            query = query.filter(Scan.id == scan_id)
            query.update({"declared_number_of_slices": (Scan.declared_number_of_slices - 1)})

    @staticmethod
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
