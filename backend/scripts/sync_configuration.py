import yaml
import logging.config
from typing import Dict, List

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Role, LabelTag


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def sync_configuration(configuration: Dict) -> None:
    """Synchronize configuration file with database entries.

    :param configuration: content of YAML configuration file
    """
    datasets = configuration.get('datasets', [])
    _sync_datasets(datasets)

    tasks = configuration.get('tasks', [])
    _sync_tasks(tasks)


def _sync_datasets(datasets: List[Dict]) -> None:
    """Synchronize Datasets from configuration file with database entries.

    Things to do:
        - add support for Tasks,
        - disabling Datasets that does not longer exists in configuration file
        - find difference in Tasks.

    :param tasks: definitions of all Datasets
    """
    with db_session() as session:
        datasets = configuration.get('datasets', [])
        for dataset in datasets:
            key = dataset.get('key', '')
            name = dataset.get('name', '')
            image_path = dataset.get('image_path', '')

            # Make sure we won't create it again!
            dataset_exists = session.query(exists().where(ScanCategory.key == key)).scalar()
            if dataset_exists:
                logger.info('Dataset exists with key "%s"', key)
                continue

            # Create this Dataset if not exists
            category = ScanCategory(key=key, name=name, image_path=image_path)
            session.add(category)
            session.commit()
            logger.info('Dataset added for key "%s"', key)


def _sync_tasks(tasks: List[Dict]) -> None:
    """Synchronize Tasks from configuration file with database entries.

    Things to do:
        - support for Tools in Label Tags,
        - disabling Tasks that does not longer exists in configuration file,
        - find differences in Tasks.

    :param tasks: definitions of all Tasks
    """
    with db_session() as session:
        for task in tasks:
            tags = task.get('tags', [])
            for tag in tags:
                key = entry.get('key', '')
                name = entry.get('name', '')

                # Make sure we won't create it again!
                tag_exists = session.query(exists().where(LabelTag.key == key)).scalar()
                if tag_exists:
                    logger.info('Label Tag exists with key "%s"', key)
                    continue

                # Create this Label tag if not exists
                tag = LabelTag(key, name)
                tag.scan_category_id = category.id
                session.add(tag)
                session.commit()
                logger.info('Label Tag added for key "%s" and assigned to category for key "%s"', key,
                            category.key)

if __name__ == '__main__':
    try:
        with open('.medtagger.yml') as config_file:
            configuration = yaml.load(config_file)
            sync_configuration(configuration)
    except yaml.YAMLError as exc:
        log.exception('Unknown error...')
