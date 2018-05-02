"""Insert all database fixtures."""
import logging.config

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Role, LabelTag

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

CATEGORIES = [{
    'key': 'KIDNEYS',
    'name': 'Kidneys',
    'image_path': '../../../assets/icon/kidneys_category_icon.svg',
}, {
    'key': 'LIVER',
    'name': 'Liver',
    'image_path': '../../../assets/icon/liver_category_icon.svg',
}, {
    'key': 'HEART',
    'name': 'Hearth',
    'image_path': '../../../assets/icon/heart_category_icon.svg',
}, {
    'key': 'LUNGS',
    'name': 'Lungs',
    'image_path': '../../../assets/icon/lungs_category_icon.svg',
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
    'category_key': 'KIDNEYS',
}, {
    'key': 'RIGHT_KIDNEY',
    'name': 'Right Kidney',
    'category_key': 'KIDNEYS',
}]


def insert_scan_categories() -> None:
    """Insert all default Scan Categories if don't exist."""
    with db_session() as session:
        for row in CATEGORIES:
            category_key = row.get('key', '')
            category_exists = session.query(exists().where(ScanCategory.key == category_key)).scalar()
            if category_exists:
                logger.info('Scan Category exists with key "%s"', category_key)
                continue

            category = ScanCategory(**row)
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
            tag_category_key = row.get('category_key', '')
            category = session.query(ScanCategory).filter(ScanCategory.key == tag_category_key).one()
            tag.scan_category_id = category.id
            session.add(tag)
            logger.info('Label Tag added for key "%s" and assigned to category for key "%s"', tag_key,
                        tag_category_key)


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
