"""Module responsible for definition of LabelTagRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import LabelTag
from medtagger.definitions import LabelTool
from medtagger.types import TaskID


def get_all_tags() -> List[LabelTag]:
    """Fetch all Label Tags from database."""
    return LabelTag.query.all()


def get_label_tag_by_key(label_tag_key: str) -> LabelTag:
    """Fetch Label Tag from database."""
    return LabelTag.query.filter(LabelTag.key == label_tag_key).one()


def add_new_tag(key: str, name: str, tools: List[LabelTool], task_id: TaskID) -> LabelTag:
    """Add new Label Tag to the database.

    :param key: key that will identify such Label Tag
    :param name: name that will be used in the User Interface for such Label Tag
    :param tools: list of tools for given LabelTag that will be available on labeling page
    :param task_id: id of Task that owns this Label Tag
    :return: Label Tag object
    """
    with db_session() as session:
        label_tag = LabelTag(key, name, tools)
        label_tag.task_id = task_id
        session.add(label_tag)
    return label_tag


def delete_tag_by_key(key: str) -> None:
    """Remove Label Tag from database."""
    with db_session() as session:
        session.query(LabelTag).filter(LabelTag.key == key).delete()


def update_tools_in_tag(key: str, tools: List[LabelTool]) -> LabelTag:
    """Update Tools that are available in Label Tag.

    :param key: key that will identify such Label Tag
    :param tools: list of tools for given LabelTag that will be available on labeling page
    :return: Label Tag object
    """
    with db_session() as session:
        label_tag = get_label_tag_by_key(key)
        label_tag.tools = tools
        session.add(label_tag)
    return label_tag


def update_name(key: str, name: str) -> LabelTag:
    """Update name of the Label Tag.

    :param key: key that will identify such Label Tag
    :param name: new name for such Label Tag
    :return: Label Tag object
    """
    with db_session() as session:
        label_tag = get_label_tag_by_key(key)
        label_tag.name = name
        session.add(label_tag)
    return label_tag


def move_to_task(key: str, task_id: TaskID) -> LabelTag:
    """Move Label Tag to the new Task.

    :param key: key that will identify such Label Tag
    :param task_id: Task ID for another Task which should be linked to this Label Tag
    :return: Label Tag object
    """
    with db_session() as session:
        label_tag = get_label_tag_by_key(key)
        label_tag.task_id = task_id
        session.add(label_tag)
    return label_tag


def disable(label_tag_key: str) -> None:
    """Disable existing Label Tag."""
    disabling_query = LabelTag.query.filter(LabelTag.key == label_tag_key)
    updated = disabling_query.update({'disabled': True}, synchronize_session='fetch')
    if not updated:
        raise Exception()  # TODO: Change me!


def enable(label_tag_key: str) -> None:
    """Enable existing Label Tag."""
    enabling_query = LabelTag.query.filter(LabelTag.key == label_tag_key)
    updated = enabling_query.update({'disabled': False}, synchronize_session='fetch')
    if not updated:
        raise Exception()  # TODO: Change me!
