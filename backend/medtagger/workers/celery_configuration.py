"""Module responsible for definition of Celery configuration."""
import os
from typing import List

from medtagger.config import AppConfiguration


def get_all_modules_with_tasks() -> List[str]:
    """Generate list of all modules with Celery tasks.

    :return: list of all modules with tasks
    """
    module_prefix = 'medtagger.workers.'
    tasks_directory = 'medtagger/workers'
    python_files = filter(lambda filename: filename.endswith('.py'), os.listdir(tasks_directory))
    return [module_prefix + os.path.splitext(filename)[0] for filename in python_files]


configuration = AppConfiguration()
broker_url = configuration.get('celery', 'broker', fallback='pyamqp://guest:guest@localhost//')
imports = get_all_modules_with_tasks()

# The default serializers for Celery >=3.1 is JSON, which doesn't make sense if we send binary data to task
task_serializer = 'pickle'
accept_content = {'pickle'}
