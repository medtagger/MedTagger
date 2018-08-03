"""Module responsible for definition of TaskRepository."""
from typing import List

from medtagger.database import db_session
from medtagger.database.models import Task, LabelTag, scan_categories_tasks


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


def add_task(key: str, name: str, image_path: str, categories_ids: List[int]) -> Task:
    """Add new Task to the database.

    :param key: key that will identify such Task
    :param name: name that will be used in the Use Interface for such Task
    :param image_path: path to the image that represents such Task (used in User Interface)
    :param categories_ids: IDs of ScanCategories that Task takes Scans from
    :return: Task object
    """
    with db_session() as session:
        task = Task(key, name, image_path)
        session.add(task)
        for category_id in categories_ids:
            # pylint: disable=no-value-for-parameter
            scan_categories_tasks.insert().values(scan_cateogory_id=category_id, task_id=task.id)
    return task


def assign_label_tag(tag: LabelTag, task_key: str) -> None:
    """Assign existing Label Tag to Task.

    :param tag: tag that should be assigned to Task
    :param task_key: key that will identify such Task
    """
    with db_session():
        task = Task.query.filter(Task.key == task_key).one()
        task.available_tags.append(tag)
        task.save()


def unassign_label_tag(tag: LabelTag, task_key: str) -> None:
    """Unassign Label Tag from Task.

    :param tag: tag that should be unassigned from Task
    :param task_key: key that will identify such Task
    """
    with db_session():
        task = Task.query.filter(Task.key == task_key).one()
        task.available_tags.remove(tag)
        task.save()
