"""Module responsible for business logic in all Tasks endpoints."""
from typing import List

from medtagger.database.models import Task, LabelTag
from medtagger.repositories import (
    tasks as TasksRepository,
)


def get_tasks() -> List[Task]:
    """Fetch all tasks.

    :return: list of tasks
    """
    return TasksRepository.get_all_tasks()


def create_task(key: str, name: str, image_path: str, categories_keys: List[str], tags: List[LabelTag]) -> Task:
    """Create new Task.

    :param key: unique key representing Task
    :param name: name which describes this Task
    :param image_path: path to the image which is located on the frontend
    :param categories_keys: Keys of ScanCategories that Task takes Scans from
    :param tags: Label Tags that will be created and assigned to Task
    :return: Task object
    """
    return TasksRepository.add_task(key, name, image_path, categories_keys, tags)
