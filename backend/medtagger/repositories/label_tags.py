"""Module responsible for definition of LabelTagRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import LabelTag
from medtagger.definitions import LabelTool
from medtagger.exceptions import InternalErrorException
from medtagger.types import TaskID


def get_all_tags(include_disabled: bool = False) -> List[LabelTag]:
    """Fetch all Label Tags from database."""
    query = LabelTag.query
    if not include_disabled:
        query = query.filter(~LabelTag.disabled)
    return query.order_by(LabelTag.key).all()


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


def update(key: str, name: str = None, tools: List[LabelTool] = None, task_id: TaskID = None) -> LabelTag:
    """Update Tools that are available in Label Tag.

    :param key: key that will identify such Label Tag
    :param name: (optional) new name for such Label Tag
    :param tools: (optional) list of tools for given LabelTag that will be available on labeling page
    :param task_id: (optional) Task ID for another Task which should be linked to this Label Tag
    :return: Label Tag object
    """
    with db_session() as session:
        label_tag = get_label_tag_by_key(key)
        if name:
            label_tag.name = name
        if tools:
            label_tag.tools = tools
        if task_id:
            label_tag.task_id = task_id
        session.add(label_tag)
    return label_tag


def disable(label_tag_key: str) -> None:
    """Disable existing Label Tag."""
    disabling_query = LabelTag.query.filter(LabelTag.key == label_tag_key)
    updated = disabling_query.update({'disabled': True}, synchronize_session='fetch')
    if not updated:
        raise InternalErrorException(f'Label Tag "{label_tag_key}" was not disabled due to unknown database error.')


def enable(label_tag_key: str) -> None:
    """Enable existing Label Tag."""
    enabling_query = LabelTag.query.filter(LabelTag.key == label_tag_key)
    updated = enabling_query.update({'disabled': False}, synchronize_session='fetch')
    if not updated:
        raise InternalErrorException(f'Label Tag "{label_tag_key}" was not enabled due to unknown database error.')
