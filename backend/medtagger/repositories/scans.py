"""Module responsible for definition of Scans' Repository."""
from typing import List

from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Scan
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
    def get_random_scan(category: ScanCategory = None) -> Scan:
        """Fetch random Scan from database.

        :param category: (optional) Scan's Category object
        :return: Label object
        """
        query = Scan.query
        if category:
            query = query.join(ScanCategory)
            query = query.filter(ScanCategory.key == category.key)
        query = query.filter(Scan.converted)
        query = query.order_by(func.random())
        return query.first()

    @staticmethod
    def delete_scan_by_id(scan_id: ScanID) -> None:
        """Remove Scan from SQL database."""
        with db_session() as session:
            session.query(Scan).filter(Scan.id == scan_id).delete()

    @staticmethod
    def add_new_scan(category: ScanCategory, number_of_slices: int) -> Scan:
        """Add new Scan to the database.

        :param category: Scan's Category object
        :param number_of_slices: number of Slices that will be uploaded
        :return: Scan object
        """
        with db_session() as session:
            scan = Scan(category, number_of_slices)
            session.add(scan)
        return scan

    @staticmethod
    def reduce_number_of_declared_slices(scan_id: ScanID) -> None:
        """Decrease number of declared Slices by one."""
        with db_session() as session:
            query = session.query(Scan)
            query = query.filter(Scan.id == scan_id)
            query.update({"declared_number_of_slices": (Scan.declared_number_of_slices - 1)})
