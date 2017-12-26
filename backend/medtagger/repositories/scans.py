"""Module responsible for definition of Scans' Repository."""
from sqlalchemy.sql.expression import func

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Scan, Slice
from medtagger.types import ScanID


class ScansRepository(object):
    """Repository for Scans."""

    @staticmethod
    def get_scan_by_id(scan_id: ScanID) -> Scan:
        """Fetch Scan from database."""
        with db_session() as session:
            scan = session.query(Scan).filter(Scan.id == scan_id).one()
        return scan

    @staticmethod
    def get_random_scan(category: ScanCategory = None) -> Scan:
        """Fetch random Scan from database.

        :param category: (optional) Scan's Category object
        :return: Label object
        """
        with db_session() as session:
            query = session.query(Scan)
            query = query.join(ScanCategory)
            if category:
                query = query.filter(ScanCategory.key == category.key)
            # All slices has to be stored and converted
            query = query.filter(~Scan.slices.any(Slice.stored.is_(False)))  # type: ignore  # No attribute `any()`
            query = query.filter(~Scan.slices.any(Slice.converted.is_(False)))  # type: ignore  # No attribute `any()`
            query = query.order_by(func.random())
            scan = query.first()
        return scan

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
