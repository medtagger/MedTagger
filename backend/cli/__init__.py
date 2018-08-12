import pkg_resources

import click

from . import (
    init as init_command,
    start as start_command,
    stop as stop_command,
    config as config_command,
)


def print_version(ctx, param, value):
    """Print current version of MedTagger."""
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require('medtagger')[0].version
    click.echo('MedTagger version: {}'.format(version))
    click.echo('GitHub page: https://github.com/jpowie01/MedTagger')
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print current version of MedTagger.')
def cli() -> None:
    """MedTagger is a collaborative framework for annotating medical datasets using crowdsourcing."""
    pass


cli.add_command(init_command.cli)
cli.add_command(start_command.cli)
cli.add_command(stop_command.cli)
cli.add_command(config_command.cli)

if __name__ == '__main__':
    cli()
