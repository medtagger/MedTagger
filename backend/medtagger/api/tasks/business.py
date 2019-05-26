"""Module responsible for business logic in all Tasks endpoints."""
# pylint: disable-msg=too-many-arguments
from typing import List

from sqlalchemy.orm.exc import NoResultFound

from medtagger.api.exceptions import NotFoundException
from medtagger.database.models import Task, LabelTag
from medtagger.repositories import (
    tasks as TasksRepository,
)


def get_tasks() -> List[Task]:
    """Fetch all tasks.

    :return: list of tasks
    """
    return TasksRepository.get_all_tasks()


def get_task_for_key(task_key: str) -> Task:
    """Fetch Task for given key.

    :return: Task
    """
    try:
        return TasksRepository.get_task_by_key(task_key)
    except NoResultFound:
        raise NotFoundException('Did not found task for {} key!'.format(task_key))


def create_task(key: str, name: str, image_path: str, datasets_keys: List[str], description: str,
                label_examples: List[str], tags: List[LabelTag]) -> Task:
    """Create new Task.

    :param key: unique key representing Task
    :param name: name which describes this Task
    :param image_path: path to the image which is located on the frontend
    :param datasets_keys: Keys of Datasets that Task takes Scans from
    :param description: Description of a given Task
    :param label_examples: List of paths to examples of labels for given Task
    :param tags: Label Tags that will be created and assigned to Task
    :return: Task object
    """
    return TasksRepository.add_task(key, name, image_path, datasets_keys, description, label_examples, tags)
