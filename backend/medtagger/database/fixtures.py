"""Insert all database fixtures."""
import logging.config
from typing import Dict, List, cast

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from medtagger.database import db_session
from medtagger.definitions import LabelTool
from medtagger.database.models import Dataset, Role, LabelTag, Task

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


TASKS = [{
    'key': 'MARK_KIDNEYS',
    'name': 'Mark kidneys',
    'image_path': 'assets/icon/kidneys_dataset_icon.svg',
}, {
    'key': 'MARK_LUNGS_NODULES',
    'name': 'Mark nodules on lungs',
    'image_path': 'assets/icon/lungs_dataset_icon.svg',
}]

DATASETS: List[Dict] = [{
    'key': 'KIDNEYS',
    'name': 'Kidneys',
    'tasks': ['MARK_KIDNEYS'],
}, {
    'key': 'LIVER',
    'name': 'Liver',
}, {
    'key': 'HEART',
    'name': 'Heart',
}, {
    'key': 'LUNGS',
    'name': 'Lungs',
    'tasks': ['MARK_LUNGS_NODULES'],
}]

ROLES = [
    {
        'name': 'admin',
    },
    {
        'name': 'doctor',
    },
    {
        'name': 'volunteer',
    },
]

TAGS = [{
    'key': 'LEFT_KIDNEY',
    'name': 'Left Kidney',
    'task_key': 'MARK_KIDNEYS',
    'tools': [LabelTool.RECTANGLE, LabelTool.POINT, LabelTool.CHAIN, LabelTool.BRUSH],
}, {
    'key': 'RIGHT_KIDNEY',
    'name': 'Right Kidney',
    'task_key': 'MARK_KIDNEYS',
    'tools': [LabelTool.RECTANGLE],
}, {
    'key': 'NODULE',
    'name': 'Nodule',
    'task_key': 'MARK_LUNGS_NODULES',
    'tools': [LabelTool.BRUSH],
}]


def insert_tasks() -> None:
    """Insert all default Tasks if don't exist."""
    with db_session() as session:
        for row in TASKS:
            task_key = row.get('key', '')
            task_exists = session.query(exists().where(Task.key == task_key)).scalar()
            if task_exists:
                logger.info('Task exists with key "%s"', task_key)
                continue

            task = Task(**row)
            session.add(task)

            logger.info('Task added for key "%s"', task_key)


def insert_datasets() -> None:
    """Insert all default Datasets if don't exist."""
    with db_session() as session:
        for row in DATASETS:
            dataset_key = row.get('key', '')
            dataset_exists = session.query(exists().where(Dataset.key == dataset_key)).scalar()
            if dataset_exists:
                logger.info('Dataset exists with key "%s"', dataset_key)
                continue

            dataset = Dataset(dataset_key, row.get('name', ''))

            tasks = row.get('tasks', [])
            for task_key in tasks:
                task = session.query(Task).filter(Task.key == task_key).one()
                dataset.tasks.append(task)

            session.add(dataset)
            logger.info('Dataset added for key "%s"', dataset_key)


def insert_labels_tags() -> None:
    """Insert all default Label Tags if they don't exist and assign them to dataset."""
    with db_session() as session:
        for row in TAGS:
            tag_key = row.get('key', '')
            tag_exists = session.query(exists().where(LabelTag.key == tag_key)).scalar()
            if tag_exists:
                logger.info('Label Tag exists with key "%s"', tag_key)
                continue

            key = cast(str, row.get('key', ''))
            name = cast(str, row.get('name', ''))
            tools = cast(List[LabelTool], row.get('tools', []))
            tag = LabelTag(key, name, tools)
            tag_task_key = row.get('task_key', '')
            task = session.query(Task).filter(Task.key == tag_task_key).one()
            tag.task_id = task.id
            session.add(tag)
            logger.info('Label Tag added for key "%s" and assigned to task for key "%s"', tag_key,
                        tag_task_key)


def insert_user_roles() -> None:
    """Insert default user Roles."""
    with db_session() as session:
        for row in ROLES:
            role_name = row.get('name', '')
            role_exists = session.query(exists().where(Role.name == role_name)).scalar()
            if role_exists:
                logger.info('Role exists with name "%s"', role_name)
                continue

            role = Role(**row)
            session.add(role)
            logger.info('Role added for name "%s"', role_name)


def apply_all_fixtures() -> None:
    """Apply all available fixtures."""
    logger.info('Applying fixtures for Tasks...')
    insert_tasks()
    logger.info('Applying fixtures for Datasets...')
    insert_datasets()
    logger.info('Applying fixtures for Label Tags...')
    insert_labels_tags()
    logger.info('Applying fixtures for user Roles...')
    insert_user_roles()


if __name__ == '__main__':
    try:
        apply_all_fixtures()
    except IntegrityError:
        logger.exception('An error occurred while applying fixtures! It is highly possible that there was'
                         'a race condition between multiple processes applying fixtures at the same time.')
