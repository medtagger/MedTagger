import subprocess

import click


@click.command('stop')
def cli():
    """Stop MedTagger on a local computer."""
    click.echo('Starting MedTagger locally...')
    docker_compose_down = subprocess.run(['docker-compose', 'down'])
    if docker_compose_down.returncode != 0:
        click.echo('Couldn\'t stop MedTagger!', err=True)
        return
