import click

from aireport import commands


@click.group()
def cli():
    click.echo('Running Project Tools')


# Add commands
cli.add_command(commands.run)
