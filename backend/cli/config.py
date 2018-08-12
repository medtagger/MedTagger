import os
import yaml
import pkg_resources
from typing import Dict, List

import click

CONFIGURATION_FILE = '.medtagger.yml'


class ConfigurationFileError(Exception):
    """Exception representing Configuration File error."""

    pass


@click.command('config')
@click.option('--validate', is_flag=True, help='Validate existing configuration')
@click.option('--generate', is_flag=True, help='Generate example configuration')
def cli(validate: bool, generate: bool) -> None:
    """Prepare or validate MedTagger configuration."""
    if not validate and not generate:
        raise click.BadParameter('You have to use one of possible flags: --validate or --generate')
    if validate:
        click.echo('Running validation...')
        validate_config()
    if generate:
        click.echo('Running generation of an example...')
        generate_example_config()


def validate_config() -> None:
    """Validate user's configuration."""
    try:
        with open(CONFIGURATION_FILE) as configuration_file:
            configuration = yaml.load(configuration_file)
            _raise_on_invalid_configuration(configuration)
        click.echo('Your configuration is fine!')
    except ConfigurationFileError as exc:
        click.echo('ERROR: Your configuration file is broken! Reason: {}'.format(exc), err=True)
        exit(1)
    except yaml.YAMLError as exc:
        click.echo('ERROR: Oops... Your file seems to be an invalid YAML file :(', err=True)
        exit(1)


def generate_example_config() -> None:
    """Generate example configuration based on example file from package."""
    # Do not override user's configuration!
    if os.path.exists(CONFIGURATION_FILE):
        click.echo('Configuration file already exists!')
        return

    # Copy content from example configuration to user's configuration
    resource_package = __name__
    resource_path = 'assets/.medtagger.yml'
    with open(CONFIGURATION_FILE, 'wb') as configuration_file:
        with pkg_resources.resource_stream(resource_package, resource_path) as example_configuration:
            configuration_file.write(example_configuration.read())
    click.echo('Configuration file saved to "{}"!'.format(CONFIGURATION_FILE))


def _raise_on_invalid_configuration(configuration: Dict) -> None:
    """Check configuration content and raise an Exception in case of issues.

    :param configuration: dictionary representation of a configuration file
    """
    tasks = configuration.get('tasks', [])
    if not isinstance(tasks, list):
        raise ConfigurationFileError('Entry "tasks" is not a List!')
    for task in tasks:
        _raise_on_invalid_task(task)

    datasets = configuration.get('datasets', [])
    if not isinstance(datasets, list):
        raise ConfigurationFileError('Entry "datasets" is not a List!')
    for dataset in datasets:
        _raise_on_invalid_dataset(dataset)


def _raise_on_invalid_task(task: Dict) -> None:
    """Check configuration of a Task.
    
    :param task: dictionary representation of a Task
    """
    task_fields = set(task.keys())
    required_task_fields = {'name', 'key', 'tags'}
    if not task_fields.issubset(required_task_fields):
        raise ConfigurationFileError('One of the Task does not have all required fields ({}).'.format(
            required_task_fields))

    if not isinstance(task['name'], str):
        raise ConfigurationFileError('Task "name" has to be string! Current value is "{}".'.format(task['name']))
    if not isinstance(task['key'], str):
        raise ConfigurationFileError('Task "key" has to be string! Current value is "{}".'.format(task['key']))
    if not isinstance(task['tags'], list):
        raise ConfigurationFileError('Task "tags" has to be list! Current value is "{}".'.format(task['tags']))

    tags = task['tags']
    for tag in tags:
        _raise_on_invalid_tag(tag)

def _raise_on_invalid_tag(tag: Dict) -> None:
    """Check configuration of a Tag.
    
    :param tag: dictionary representation of a Tag
    """
    tag_fields = set(tag.keys())
    required_tag_fields = {'name', 'key', 'tools'}
    if not tag_fields.issubset(required_tag_fields):
        raise ConfigurationFileError('One of the Tag does not have all required fields ({}).'.format(
            required_tag_fields))

    if not isinstance(tag['name'], str):
        raise ConfigurationFileError('Tag "name" has to be string! Current value is "{}".'.format(tag['name']))
    if not isinstance(tag['key'], str):
        raise ConfigurationFileError('Tag "key" has to be string! Current value is "{}".'.format(tag['key']))
    if not isinstance(tag['tools'], list):
        raise ConfigurationFileError('Tag "tools" has to be list! Current value is "{}".'.format(tag['tags']))

    tools = tag['tools']
    for tool in tools:
        if not isinstance(tool, str):
            raise ConfigurationFileError('Tool "{}" is not a string value!'.format(tool))


def _raise_on_invalid_dataset(dataset: Dict) -> None:
    """Check configuration of a Tag.

    TODO:
        - check if Tasks exists on list of all Tasks.
    
    :param tag: dictionary representation of a Tag
    """
    dataset_fields = set(dataset.keys())
    required_dataset_fields = {'name', 'key', 'image_path', 'tasks'}
    if not dataset_fields.issubset(required_dataset_fields):
        raise ConfigurationFileError('One of the Dataset does not have all required fields ({}).'.format(
            required_dataset_fields))

    if not isinstance(dataset['name'], str):
        raise ConfigurationFileError('Dataset "name" has to be string! Current value is "{}".'.format(dataset['name']))
    if not isinstance(dataset['key'], str):
        raise ConfigurationFileError('Dataset "key" has to be string! Current value is "{}".'.format(dataset['key']))
    if not isinstance(dataset['image_path'], str):
        raise ConfigurationFileError('Dataset "image_path" has to be string! Current value is "{}".'.format(dataset['image_path']))
    if not isinstance(dataset['tasks'], list):
        raise ConfigurationFileError('Dataset "tasks" has to be list! Current value is "{}".'.format(dataset['tasks']))

    tasks = dataset['tasks']
    for task in tasks:
        if not isinstance(task, str):
            raise ConfigurationFileError('Task "{}" is not a string value!'.format(task))
