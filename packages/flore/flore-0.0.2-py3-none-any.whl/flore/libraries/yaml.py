import os
import pathlib

import click

from .base import Base


class Yaml(Base):
    def __init__(self) -> None:
        self.migration_dir = None
        self.files = ("migration.yaml", "seed.yaml", "config.yaml")

    def open(self):
        self.migration_dir = "migrations"
        if not os.path.exists(self.migration_dir):
            os.mkdir(self.migration_dir)

    def create(self):
        if self.migration_dir:
            for file in self.files:
                file = os.path.join(self.migration_dir, file)
                if not os.path.exists(file):
                    pathlib.Path(file).touch()
                    click.echo(f"{file} created successfully")
                else:
                    click.echo("we need create nothing.look like good :)")
                    break
