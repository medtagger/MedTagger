"""Module responsible for definition of ScanCategoriesRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import ScanCategory


def get_all_categories(include_disabled: bool = False) -> List[ScanCategory]:
    """Return list of all Scan Categories."""
    with db_session() as session:
        query = session.query(ScanCategory)
        if not include_disabled:
            query = query.filter(~ScanCategory.disabled)
        categories = query.order_by(ScanCategory.id).all()
    return categories


def get_category_by_key(key: str) -> ScanCategory:
    """Fetch Scan Category from database.

    :param key: key for a Scan Category
    :return: Scan Category object
    """
    with db_session() as session:
        category = session.query(ScanCategory).filter(ScanCategory.key == key).one()
    return category


def add_new_category(key: str, name: str) -> ScanCategory:
    """Add new Scan Category to the database.

    :param key: key that will identify such Scan Category
    :param name: name that will be used in the Use Interface for such Scan Category
    :return: Scan Category object
    """
    with db_session() as session:
        category = ScanCategory(key, name)
        session.add(category)
    return category


def disable(scan_category_key: str):
    """Disable existing Scan Category."""
    disabling_query = ScanCategory.query.filter(ScanCategory.key == scan_category_key)
    updated = disabling_query.update({'disabled': True}, synchronize_session='fetch')
    if not updated:
        raise Exception()  # TODO: Change me!


def enable(scan_category_key: str) -> None:
    """Enable existing Scan Category."""
    enabling_query = ScanCategory.query.filter(ScanCategory.key == scan_category_key)
    updated = enabling_query.update({'disabled': False}, synchronize_session='fetch')
    if not updated:
        raise Exception()  # TODO: Change me!
