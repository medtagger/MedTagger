"""Module responsible for definition of LabelTagRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import LabelTag
from medtagger.definitions import LabelTool


def get_all_tags() -> List[LabelTag]:
    """Fetch all Label Tags from database."""
    return LabelTag.query.all()


def get_label_tag_by_key(label_tag_key: str) -> LabelTag:
    """Fetch Label Tag from database."""
    return LabelTag.query.filter(LabelTag.key == label_tag_key).one()


def add_new_tag(key: str, name: str, tools: List[LabelTool]) -> LabelTag:
    """Add new Label Tag to the database.

    :param key: key that will identify such Label Tag
    :param name: name that will be used in the User Interface for such Label Tag
    :param tools: list of tools for given LabelTag that will be available on labeling page
    :return: Label Tag object
    """
    with db_session() as session:
        label_tag = LabelTag(key, name, tools)
        session.add(label_tag)
    return label_tag


def delete_tag_by_key(key: str) -> None:
    """Remove Label Tag from database."""
    with db_session() as session:
        session.query(LabelTag).filter(LabelTag.key == key).delete()
