import click
import yaml
from dbks.cluster.controller import ClusterController


ctl = ClusterController()


@click.group()
def cli():
    """Commands for Databricks cluster operations."""
    pass


@cli.command()
@click.argument("yml_path", type=click.Path(exists=True))
@click.option(
    "--pin", type=click.BOOL, default="true", help="Pin cluster", show_default=True
)
def create_or_edit_from_yml(yml_path, pin):
    """\b
    Parse a YAML file and use its content to create or edit cluster(s).
    Please refer to documentation for YAML file example.
    """
    with open(yml_path) as file:
        clusters_to_deploy = yaml.load(file, Loader=yaml.FullLoader)
    for cluster_name, cluster_def in clusters_to_deploy.items():
        ctl.create_or_edit_cluster(cluster_def=cluster_def, pin=pin)


@cli.command()
@click.argument("cluster_name", type=str, required=True)
def delete_by_name(cluster_name):
    """Delete a cluster by name."""
    ctl.delete_by_name(cluster_name)
