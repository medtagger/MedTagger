import subprocess

import click


@click.command('start')
def cli():
    """Start MedTagger on a local computer."""
    click.echo('Starting MedTagger locally...')
    docker_compose_up = subprocess.run(['docker-compose', 'up', '-d'])
    if docker_compose_up.returncode != 0:
        click.echo('Couldn\'t start MedTagger!', err=True)
        return
