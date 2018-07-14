"""Module responsible for definition of TaskRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Task


def get_all_tasks() -> List[Task]:
    """Fetch all tasks from database ordered by id."""
    with db_session() as session:
        tasks = session.query(Task).order_by(Task.id).all()
    return tasks


def get_task_by_key(key: str) -> Task:
    """Fetch Task from database.

    :param key: key for a Task
    :return: Task object
    """
    with db_session() as session:
        task = session.query(Task).filter(Task.key == key).one()
    return task


def add_task(key: str, name: str, image_path: str) -> Task:
    with db_session() as session:
        task = Task(key, name, image_path)
        session.add(task)
    return task



