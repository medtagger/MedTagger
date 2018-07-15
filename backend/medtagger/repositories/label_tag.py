"""Module responsible for definition of Label Tags Repository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import LabelTag


class LabelTagRepository:
    """Repository for Label Tags."""

    @staticmethod
    def get_all_tags() -> List[LabelTag]:
        """Fetch all Label Tags from database."""
        return LabelTag.query.all()

    @staticmethod
    def get_label_tag_by_key(label_tag_key: str) -> LabelTag:
        """Fetch Label Tag from database."""
        return LabelTag.query.filter(LabelTag.key == label_tag_key).one()

    @staticmethod
    def add_new_tag(key: str, name: str) -> LabelTag:
        """Add new Label Tag to the database.

        :param key: key that will identify such Label Tag
        :param name: name that will be used in the User Interface for such Label Tag
        :return: Label Tag object
        """
        with db_session() as session:
            label_tag = LabelTag(key, name)
            session.add(label_tag)
        return label_tag

    @staticmethod
    def delete_tag_by_key(key: str) -> None:
        """Remove Label Tag from database."""
        with db_session() as session:
            session.query(LabelTag).filter(LabelTag.key == key).delete()
