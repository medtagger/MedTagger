"""Module responsible for definition of ScanCategoriesRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import ScanCategory


def get_all_categories() -> List[ScanCategory]:
    """Return list of all Scan Categories."""
    with db_session() as session:
        categories = session.query(ScanCategory).order_by(ScanCategory.id).all()
    return categories


def get_category_by_key(key: str) -> ScanCategory:
    """Fetch Scan Category from database.

    :param key: key for a Scan Category
    :return: Scan Category object
    """
    with db_session() as session:
        category = session.query(ScanCategory).filter(ScanCategory.key == key).one()
    return category


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
