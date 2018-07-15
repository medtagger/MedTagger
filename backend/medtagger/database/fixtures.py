"""Insert all database fixtures."""
import logging.config
from typing import Dict, List

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Role, LabelTag, Task

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


TASKS = [{
    'key': 'MARK_KIDNEYS',
    'name': 'Mark kidneys',
    'image_path': 'assets/icon/kidneys_category_icon.svg',
}]

CATEGORIES: List[Dict] = [{
    'key': 'KIDNEYS',
    'name': 'Kidneys',
    'image_path': 'assets/icon/kidneys_category_icon.svg',
    'tasks': ['MARK_KIDNEYS'],
}, {
    'key': 'LIVER',
    'name': 'Liver',
    'image_path': 'assets/icon/liver_category_icon.svg',
    'tasks': [],
}, {
    'key': 'HEART',
    'name': 'Heart',
    'image_path': 'assets/icon/heart_category_icon.svg',
    'tasks': [],
}, {
    'key': 'LUNGS',
    'name': 'Lungs',
    'image_path': 'assets/icon/lungs_category_icon.svg',
    'tasks': [],
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
}, {
    'key': 'RIGHT_KIDNEY',
    'name': 'Right Kidney',
    'task_key': 'MARK_KIDNEYS',
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


def insert_scan_categories() -> None:
    """Insert all default Scan Categories if don't exist."""
    with db_session() as session:
        for row in CATEGORIES:
            category_key = row.get('key', '')
            category_exists = session.query(exists().where(ScanCategory.key == category_key)).scalar()
            if category_exists:
                logger.info('Scan Category exists with key "%s"', category_key)
                continue

            category = ScanCategory(category_key, row.get('name', ''), row.get('image_path', ''))

            tasks = row.get('tasks', [])
            for task_key in tasks:
                task = session.query(Task).filter(Task.key == task_key).one()
                category.tasks.append(task)

            session.add(category)
            logger.info('Scan Category added for key "%s"', category_key)


def insert_labels_tags() -> None:
    """Insert all default Label Tags if they don't exist and assign them to category."""
    with db_session() as session:
        for row in TAGS:
            tag_key = row.get('key', '')
            tag_exists = session.query(exists().where(LabelTag.key == tag_key)).scalar()
            if tag_exists:
                logger.info('Label Tag exists with key "%s"', tag_key)
                continue

            tag = LabelTag(row.get('key', ''), row.get('name', ''))
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
    logger.info('Applying fixtures for Scan Categories...')
    insert_scan_categories()
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
