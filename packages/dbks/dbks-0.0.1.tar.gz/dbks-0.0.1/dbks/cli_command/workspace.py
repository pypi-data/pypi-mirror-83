import click
from dbks.workspace.controller import WorkspaceController


ctl = WorkspaceController()


@click.group()
def cli():
    """Commands for Databricks workspace operations."""
    pass


@cli.command()
@click.argument("path")
def mkdirs(path):
    """Create workspace folder."""
    ctl.mkdirs(path)
