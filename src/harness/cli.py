import json

import click

from .clickup import ClickUpClient
from .config import Config


def _client() -> ClickUpClient:
    return ClickUpClient(Config.from_env().clickup_api_token)


# ClickUp's native priority field is an integer: 1=urgent ... 4=low.
CLICKUP_PRIORITY = {"urgent": 1, "high": 2, "normal": 3, "low": 4}


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
@click.option("--team-id", default=None, help="Defaults to CLICKUP_TEAM_ID from .env.")
def spaces(team_id: str | None):
    team_id = team_id or Config.from_env().clickup_team_id
    if not team_id:
        raise click.UsageError("Provide --team-id or set CLICKUP_TEAM_ID in .env.")
    click.echo(json.dumps(_client().get_spaces(team_id), indent=2))


@clickup.command("folders")
@click.option("--space-id", required=True)
def folders(space_id: str):
    click.echo(json.dumps(_client().get_folders(space_id), indent=2))


@clickup.command("lists")
@click.option("--space-id", default=None)
@click.option("--folder-id", default=None)
def lists(space_id: str | None, folder_id: str | None):
    click.echo(json.dumps(_client().get_lists(space_id=space_id, folder_id=folder_id), indent=2))


@clickup.command("get-task")
@click.option("--task-id", required=True)
def get_task(task_id: str):
    click.echo(json.dumps(_client().get_task(task_id), indent=2))


@clickup.command("tasks")
@click.option("--list-id", required=True)
def tasks(list_id: str):
    click.echo(json.dumps(_client().get_tasks(list_id), indent=2))


@clickup.command("create-task")
@click.option("--list-id", default=None, help="Defaults to CLICKUP_LIST_ID from .env.")
@click.option("--name", required=True)
@click.option("--description", default=None)
@click.option(
    "--priority",
    type=click.Choice(list(CLICKUP_PRIORITY)),
    default=None,
    help="ClickUp priority: urgent, high, normal, or low.",
)
def create_task(list_id: str | None, name: str, description: str | None, priority: str | None):
    list_id = list_id or Config.from_env().clickup_list_id
    if not list_id:
        raise click.UsageError("Provide --list-id or set CLICKUP_LIST_ID in .env.")
    fields = {}
    if priority is not None:
        fields["priority"] = CLICKUP_PRIORITY[priority]
    task = _client().create_task(list_id, name, description, **fields)
    click.echo(json.dumps(task, indent=2))


if __name__ == "__main__":
    cli()
