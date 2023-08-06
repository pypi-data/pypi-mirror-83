import os
import click


class ComplexCLI(click.MultiCommand):
    def list_commands(self, ctx):
        files = []
        for file_name in os.listdir(
            os.path.join(os.path.dirname(__file__), "cli_command")
        ):
            if file_name.endswith(".py") and not file_name.startswith("__"):
                files.append(file_name[:-3])
        files.sort()
        return files

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"dbks.cli_command.{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
def cli():
    """\b
    ===============================
    ==  dbks - a Databricks CLI  ==
    ==============================="""
    pass
