"""Module responsible for definition of ScanCategoriesRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, LabelTag


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


def assign_label_tag(tag: LabelTag, scan_category_key: str) -> None:
    """Assign existing Label Tag to Scan Category.

    :param tag: tag that should be assigned to Scan Category
    :param scan_category_key: key that will identify such Scan Category
    """
    scan_category = ScanCategory.query.filter(ScanCategory.key == scan_category_key).one()
    scan_category.available_tags.append(tag)
    scan_category.save()


def unassign_label_tag(tag: LabelTag, scan_category_key: str) -> None:
    """Unassign Label Tag from Scan Category.

    :param tag: tag that should be unassigned from Scan Category
    :param scan_category_key: key that will identify such Scan Category
    """
    scan_category = ScanCategory.query.filter(ScanCategory.key == scan_category_key).one()
    scan_category.available_tags.remove(tag)
    scan_category.save()
