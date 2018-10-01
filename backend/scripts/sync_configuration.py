"""Script for MedTagger's configuration synchronization."""
import argparse
import logging.config
from typing import Dict

import yaml
from sqlalchemy.exc import IntegrityError

from medtagger.database.models import Task
from medtagger.definitions import LabelTool
from medtagger.repositories import (
    datasets as DatasetsRepository,
    tasks as TasksRepository,
    label_tags as LabelTagsRepository,
)
from medtagger.types import TaskID

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

DEFAULT_CONFIGURATION_FILE_NAME = '.medtagger.yml'


def sync_configuration(configuration: Dict) -> None:
    """Synchronize configuration file with database entries.

    :param configuration: content of YAML configuration file
    """
    logger.info('Running Configuration Synchronization...')
    _sync_datasets(configuration)
    _sync_tasks(configuration)


def _sync_datasets(configuration: Dict) -> None:
    """Synchronize Datasets from configuration file with database entries.

    Example DataSets in the configuration file:
    ```
    datasets:
      - name: Kidneys
        key: KIDNEYS
        tasks:
          - KIDNEYS_SEGMENTATION
    ```

    :param configuration: content of YAML configuration file
    """
    datasets = configuration.get('datasets', []) or []
    configuration_datasets_keys = {dataset['key'] for dataset in datasets}
    database_datasets_keys = {dataset.key for dataset in DatasetsRepository.get_all_datasets(include_disabled=True)}

    datasets_to_add = configuration_datasets_keys - database_datasets_keys
    datasets_to_disable = database_datasets_keys - configuration_datasets_keys
    datasets_to_enable = database_datasets_keys & configuration_datasets_keys

    for dataset_key in datasets_to_add:
        dataset = next(dataset for dataset in datasets if dataset['key'] == dataset_key)
        DatasetsRepository.add_new_dataset(dataset['key'], dataset['name'])
        logger.info('New DataSet added: %s', dataset['key'])

    for dataset_key in datasets_to_enable:
        dataset = next(dataset for dataset in datasets if dataset['key'] == dataset_key)
        DatasetsRepository.enable(dataset['key'])
        DatasetsRepository.update(dataset['key'], dataset['name'])
        logger.info('DataSet enabled: %s', dataset['key'])

    for dataset_key in datasets_to_disable:
        DatasetsRepository.disable(dataset_key)
        logger.info('DataSet disabled: %s', dataset_key)


def _sync_tasks(configuration: Dict) -> None:
    """Synchronize Tasks from configuration file with database entries.

    Example Tasks in the configuration file:
    ```
    tasks:
      - key: KIDNEYS_SEGMENTATION
        name: Kidneys segmentation
        image_path: assets/icon/kidneys_dataset_icon.svg
        tags:
          - key: LEFT_KIDNEY
            name: Left Kidney
            tools:
              - CHAIN
          - key: RIGHT_KIDNEY
            name: Right Kidney
            tools:
              - CHAIN
    ```

    :param configuration: content of YAML configuration file
    """
    datasets = configuration.get('datasets', []) or []
    tasks = configuration.get('tasks', []) or []
    configuration_tasks_keys = {task['key'] for task in tasks}
    database_tasks_keys = {task.key for task in Task.query.all()}

    tasks_to_add = configuration_tasks_keys - database_tasks_keys
    tasks_to_disable = database_tasks_keys - configuration_tasks_keys
    tasks_to_enable = database_tasks_keys & configuration_tasks_keys

    # Add all new Tasks that haven't ever been in the DB
    for task_key in tasks_to_add:
        task = next(task for task in tasks if task['key'] == task_key)
        datasets_keys = [dataset['key'] for dataset in datasets if task['key'] in dataset['tasks']]
        TasksRepository.add_task(task['key'], task['name'], task['image_path'], datasets_keys, [])
        _sync_label_tags_in_task(configuration, task_key)
        logger.info('New Task added: %s', task['key'])

    # Enable back all Tasks that were previously commented-out or removed from configuration file
    for task_key in tasks_to_enable:
        TasksRepository.enable(task_key)
        _sync_label_tags_in_task(configuration, task_key)
        task = next(task for task in tasks if task['key'] == task_key)
        datasets_keys = [dataset['key'] for dataset in datasets if task['key'] in dataset['tasks']]
        TasksRepository.update(task_key, task['name'], task['image_path'], datasets_keys)
        logger.info('Task enabled: %s', task_key)

    # Disable all Tasks that exists in the DB but are missing in configuration file
    for task_key in tasks_to_disable:
        TasksRepository.disable(task_key)
        task = TasksRepository.get_task_by_key(task_key)
        for tag in task.available_tags:
            LabelTagsRepository.disable(tag.key)
            logger.info('LabelTag disabled: %s', tag.key)
        logger.info('Task disabled: %s', task_key)


def _sync_label_tags_in_task(configuration: Dict, task_key: str) -> None:
    """Synchronize Label Tags in given Task based on configuration file and database entries.

    :param configuration: content of YAML configuration file
    :param task_key: key for the Task that should be synchronized
    """
    db_task = TasksRepository.get_task_by_key(task_key)
    configuration_task = next(task for task in configuration['tasks'] if task['key'] == task_key)
    configuration_tags_keys = {tag['key'] for tag in configuration_task['tags']}
    database_tags_keys = {tag.key for tag in db_task.available_tags}

    tags_to_add = configuration_tags_keys - database_tags_keys
    tags_to_disable = database_tags_keys - configuration_tags_keys
    tags_to_enable = database_tags_keys & configuration_tags_keys

    for tag_key in tags_to_add:
        tag = next(tag for tag in configuration_task['tags'] if tag_key == tag['key'])
        _add_label_tag(tag, db_task.id)
        logger.info('New LabelTag added: %s', tag_key)

    for tag_key in tags_to_disable:
        LabelTagsRepository.disable(tag_key)
        logger.info('LabelTag disabled: %s', tag_key)

    for tag_key in tags_to_enable:
        tag = next(tag for tag in configuration_task['tags'] if tag_key == tag['key'])
        tools = [LabelTool[tool] for tool in tag['tools']]
        LabelTagsRepository.enable(tag_key)
        LabelTagsRepository.update(tag_key, tag['name'], tools)
        logger.info('LabelTag enabled: %s', tag_key)


def _add_label_tag(tag: Dict, db_task_id: TaskID) -> None:
    """Add Label Tag or reuse previously created one.

    :param tag: configuration of a Label Tag
    :param db_task_id: TaskID which should be connected with this Label Tag
    """
    tools = [LabelTool[tool] for tool in tag['tools']]
    try:
        LabelTagsRepository.add_new_tag(tag['key'], tag['name'], tools, db_task_id)
    except IntegrityError:
        # Such Label Tag could be previously used in another Task
        logger.warning('Reusing previously existing Label Tag (%s)! This may cause data inconsistency! '
                       'Make sure you know what you are doing and clear database entries if necessary!',
                       tag['key'])
        LabelTagsRepository.update(tag['key'], tag['name'], tools, db_task_id)
        LabelTagsRepository.enable(tag['key'])


def run() -> None:
    """Entry point for this script."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--configuration', type=str, default=DEFAULT_CONFIGURATION_FILE_NAME)
    arguments = parser.parse_args()

    try:
        with open(arguments.configuration) as config_file:
            configuration = yaml.load(config_file)
            sync_configuration(configuration)
    except yaml.YAMLError:
        logger.exception('Invalid MedTagger configuration file format.')


if __name__ == '__main__':
    run()
