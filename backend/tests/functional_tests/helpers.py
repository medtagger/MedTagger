"""Helpers functions for functional tests."""
from medtagger.database.models import LabelTag
from medtagger.repositories import label_tags as LabelTagsRepository, tasks as TasksRepository


def create_tag_and_assign_to_task(key: str, name: str, task_key: str) -> LabelTag:
    """Create Label Tag and assign it to Task.

    :param key: key that will identify such Label Tag
    :param name: name that will be used in the User Interface for such Label Tag
    :param task_key: key of the Task that Label Tag will be assigned to
    :return: Label Tag
    """
    label_tag = LabelTagsRepository.add_new_tag(key, name)
    TasksRepository.assign_label_tag(label_tag, task_key)
    return label_tag
