import click
from aireport.main import tools_ui


@click.command()
def run():
    tools_ui()
