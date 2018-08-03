import yaml
import logging.config
from typing import Dict, List

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from medtagger.database import db_session
from medtagger.database.models import ScanCategory, Role, LabelTag
from medtagger.repositories import scan_categories as ScanCategoriesRepository


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def sync_configuration(configuration: Dict) -> None:
    """Synchronize configuration file with database entries.

    :param configuration: content of YAML configuration file
    """
    logger.info('Running Configuration Synchronization...')

    datasets = configuration.get('datasets', [])
    _sync_datasets(datasets)

    # tasks = configuration.get('tasks', [])
    # _sync_tasks(tasks)


def _sync_datasets(datasets: List[Dict]) -> None:
    """Synchronize Datasets from configuration file with database entries.

    Example DataSets in the configuration file:
    ```
    datasets:
      - name: Kidneys
        key: KIDNEYS
        image_path: assets/icon/kidneys_category_icon.svg
        tasks:
          - KIDNEYS_SEGMENTATION
    ```

    :param tasks: definitions of all Datasets
    """
    datasets = configuration.get('datasets', [])
    configuration_datasets_keys = {dataset['key'] for dataset in datasets}
    database_datasets_keys = {dataset.key for dataset in ScanCategory.query.all()}

    datasets_to_add = configuration_datasets_keys - database_datasets_keys
    datasets_to_disable = database_datasets_keys - configuration_datasets_keys
    datasets_to_enable = database_datasets_keys & configuration_datasets_keys

    for dataset in datasets:
        if dataset['key'] in datasets_to_add:
            ScanCategoriesRepository.add_new_category(dataset['key'], dataset['name'], dataset['image_path'])
            logger.info('New DataSet added: %s', dataset['key'])
        elif dataset['key'] in datasets_to_disable:
            ScanCategoriesRepository.disable(dataset['key'])
            logger.info('DataSet disabled: %s', dataset['key'])
        elif dataset['key'] in datasets_to_enable:
            ScanCategoriesRepository.enable(dataset['key'])
            logger.info('DataSet enabled: %s', dataset['key'])

    # TODO: Find out difference in Tasks (Piotr patch is needed here!)


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
