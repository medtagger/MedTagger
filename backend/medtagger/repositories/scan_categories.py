"""Module responsible for definition of Scan Categories' Repository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, LabelTag


class ScanCategoriesRepository(object):
    """Repository for Scan Categories."""

    @staticmethod
    def get_all_categories() -> List[ScanCategory]:
        """Return list of all Scan Categories."""
        with db_session() as session:
            categories = session.query(ScanCategory).order_by(ScanCategory.id).all()
        return categories

    @staticmethod
    def get_category_by_key(key: str) -> ScanCategory:
        """Fetch Scan Category from database.

        :param key: key for a Scan Category
        :return: Scan Category object
        """
        with db_session() as session:
            category = session.query(ScanCategory).filter(ScanCategory.key == key).one()
        return category

    @staticmethod
    def add_new_category(key: str, name: str, image_path: str) -> ScanCategory:
        """Add new Scan Category to the database.

        :param key: key that will identify such Scan Category
        :param name: name that will be used in the Use Interface for such Scan Category
        :param image_path: path to the image that represents such Scan Category (used in User Interface)
        :return: Scan Category object
        """
        with db_session() as session:
            category = ScanCategory(key, name, image_path)
            session.add(category)
        return category

    @staticmethod
    def add_tag(tag: LabelTag, key: str) -> None:
        """Add Label Tag to Scan Category.

        :param tag: tag that should be added to Scan Category
        :param key: key that will identify such Scan Category
        """
        with db_session() as session:
            query = session.query(ScanCategory)
            query = query.filter(ScanCategory.key == key).one()
            query.update({tag: (ScanCategory.available_tags.append(tag))})

    @staticmethod
    def remove_tag(tag: LabelTag, key: str) -> None:
        """Remove Label Tag from Scan Category.

        :param tag: tag that should be removed from Scan Category
        :param key: key that will identify such Scan Category
        """
        with db_session() as session:
            query = session.query(ScanCategory)
            query = query.filter(ScanCategory.key == key).one()
            query.update({tag: (ScanCategory.available_tags.remove(tag))})
