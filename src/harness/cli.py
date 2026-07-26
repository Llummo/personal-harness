import json

import click

from .clickup import ClickUpClient
from .config import Config


def _client() -> ClickUpClient:
    return ClickUpClient(Config.from_env().clickup_api_token)


@click.group()
def cli():
    """Personal harness: ClickUp ticket automation and QA tooling."""


@cli.group()
def clickup():
    """ClickUp operations."""


@clickup.command("teams")
def teams():
    click.echo(json.dumps(_client().get_teams(), indent=2))


@clickup.command("spaces")
@click.option("--team-id", required=True)
def spaces(team_id: str):
    click.echo(json.dumps(_client().get_spaces(team_id), indent=2))


@clickup.command("lists")
@click.option("--space-id", default=None)
@click.option("--folder-id", default=None)
def lists(space_id: str | None, folder_id: str | None):
    click.echo(json.dumps(_client().get_lists(space_id=space_id, folder_id=folder_id), indent=2))


@clickup.command("create-task")
@click.option("--list-id", required=True)
@click.option("--name", required=True)
@click.option("--description", default=None)
def create_task(list_id: str, name: str, description: str | None):
    task = _client().create_task(list_id, name, description)
    click.echo(json.dumps(task, indent=2))


if __name__ == "__main__":
    cli()
