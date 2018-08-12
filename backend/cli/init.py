import os
import subprocess
import pkg_resources

import click

DOCKER_COMPOSE_FILE = 'docker-compose.yml'
DOCKER_COMPOSE_ENV_FILE = 'medtagger.env'


@click.command('init')
def cli():
    """Initialize MedTagger on a local computer."""
    click.echo('Checking for Docker & Docker Compose...')
    docker_version = subprocess.run(['docker', '--version'])
    if docker_version.returncode != 0:
        click.echo('Couldn\'t find Docker!', err=True)
        return
    docker_compose_version = subprocess.run(['docker-compose', '--version'])
    if docker_compose_version.returncode != 0:
        click.echo('Couldn\'t find Docker Compose!', err=True)
        return

    click.echo('Preparing example configuration for Docker Compose...')
    if os.path.exists(DOCKER_COMPOSE_FILE):
        click.echo('Docker Compose file already exists! Skipping!')
    else:
        resource_package = __name__
        resource_path = 'assets/docker-compose.yml'
        with open(DOCKER_COMPOSE_FILE, 'wb') as docker_compose_file:
            with pkg_resources.resource_stream(resource_package, resource_path) as example_docker_compose:
                docker_compose_file.write(example_docker_compose.read())

    click.echo('Preparing Docker Compose environment settings...')
    if os.path.exists(DOCKER_COMPOSE_ENV_FILE):
        click.echo('Docker Compose environment settings already exists! Skipping!')
    else:
        resource_package = __name__
        resource_path = 'assets/medtagger.env'
        with open(DOCKER_COMPOSE_ENV_FILE, 'wb') as docker_compose_file_env:
            with pkg_resources.resource_stream(resource_package, resource_path) as example_docker_compose_env:
                docker_compose_file_env.write(example_docker_compose_env.read())

    click.echo('Initializing configuration...')
    configuration_generation = subprocess.run(['medtagger', 'config', '--generate'])
    if configuration_generation.returncode != 0:
        click.echo('Configuration generation failed due to unknown issue!', err=True)
        return

    click.echo('Pulling Docker images...')
    docker_pull = subprocess.run(['docker-compose', 'pull'])
    if docker_pull.returncode != 0:
        click.echo('Pulling Docker images failed due to unknown issue!', err=True)
        return
