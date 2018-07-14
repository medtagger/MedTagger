"""Helpers functions for functional tests."""
from medtagger.database.models import LabelTag
from medtagger.repositories import label_tags as LabelTagsRepository, scan_categories as ScanCategoriesRepository


def create_tag_and_assign_to_category(key: str, name: str, scan_category_key: str) -> LabelTag:
    """Create Label Tag and assign it to Scan Category.

    :param key: key that will identify such Label Tag
    :param name: name that will be used in the User Interface for such Label Tag
    :param scan_category_key: key of the Scan Category that Label Tag will be assigned to
    :return: Label Tag
    """
    label_tag = LabelTagsRepository.add_new_tag(key, name)
    ScanCategoriesRepository.assign_label_tag(label_tag, scan_category_key)
    return label_tag
