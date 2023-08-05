import click
from yaml import safe_load

from flore.facede import facede
from flore.libraries.pg import Postgres
from flore.libraries.yaml import Yaml
from flore.utils import open_yaml_file


@click.group()
def flore_cli():
    """A great option for creating SQL tables in toml format."""


@flore_cli.command(help="create flore folder")
def init():
    facede(Yaml())


@flore_cli.command(help="run script to export your migrations to database")
def run():
    config = safe_load(open_yaml_file("config.yaml"))
    tables = safe_load(open_yaml_file("migration.yaml"))
    facede(Postgres(config, tables["tables"]))
