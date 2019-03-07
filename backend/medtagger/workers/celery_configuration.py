"""Module responsible for definition of Celery configuration."""
import os
import logging.config
from typing import List, Any

from celery.signals import setup_logging, worker_process_init

from medtagger.config import AppConfiguration
from medtagger.database import engine
from medtagger.storage import create_connection


def get_all_modules_with_tasks() -> List[str]:
    """Generate list of all modules with Celery tasks.

    :return: list of all modules with tasks
    """
    module_prefix = 'medtagger.workers.'
    tasks_directory = 'medtagger/workers'
    python_files = filter(lambda filename: filename.endswith('.py'), os.listdir(tasks_directory))
    return [module_prefix + os.path.splitext(filename)[0] for filename in python_files]


@setup_logging.connect
def setup_logging_handler(*args: List[Any], **kwargs: List[Any]) -> None:  # pylint: disable=unused-argument
    """Set up logger for Celery tasks."""
    logging.config.fileConfig('logging.conf')


@worker_process_init.connect
def process_initialization(*args: List[Any], **kwargs: List[Any]) -> None:  # pylint: disable=unused-argument
    """Initialize given Celery process."""
    create_connection()
    engine.dispose()  # Recreate SQL Pool


configuration = AppConfiguration()
broker_url = configuration.get('celery', 'broker', fallback='pyamqp://guest:guest@localhost//')
imports = get_all_modules_with_tasks()
