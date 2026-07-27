import json

import click

from .clickup import ClickUpClient
from .config import Config, LinearConfig
from .linear import LINEAR_PRIORITY, LinearClient


def _client() -> ClickUpClient:
    return ClickUpClient(Config.from_env().clickup_api_token)


def _linear_client() -> LinearClient:
    return LinearClient(LinearConfig.from_env().linear_api_key)


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
@click.option("--assignees", default=None, help="Comma-separated ClickUp user IDs.")
@click.option("--due-date", default=None, type=int, help="Due date as a Unix timestamp in milliseconds.")
@click.option("--parent", default=None, help="ClickUp task id to nest this task under as a subtask.")
def create_task(
    list_id: str | None,
    name: str,
    description: str | None,
    priority: str | None,
    assignees: str | None,
    due_date: int | None,
    parent: str | None,
):
    list_id = list_id or Config.from_env().clickup_list_id
    if not list_id:
        raise click.UsageError("Provide --list-id or set CLICKUP_LIST_ID in .env.")
    fields = {}
    if priority is not None:
        fields["priority"] = CLICKUP_PRIORITY[priority]
    if assignees:
        fields["assignees"] = [int(a) for a in assignees.split(",") if a.strip()]
    if due_date is not None:
        fields["due_date"] = due_date
    if parent:
        fields["parent"] = parent
    task = _client().create_task(list_id, name, description, **fields)
    click.echo(json.dumps(task, indent=2))


@clickup.command("set-status")
@click.option("--task-id", required=True)
@click.option("--status", required=True, help="A status name valid for the task's list, e.g. \"done\".")
def set_status(task_id: str, status: str):
    task = _client().update_task_status(task_id, status)
    click.echo(json.dumps(task, indent=2))


@cli.group()
def linear():
    """Linear operations."""


@linear.command("viewer")
def linear_viewer():
    click.echo(json.dumps(_linear_client().get_viewer(), indent=2))


@linear.command("teams")
def linear_teams():
    click.echo(json.dumps(_linear_client().get_teams(), indent=2))


@linear.command("states")
@click.option("--team-id", required=True)
def linear_states(team_id: str):
    click.echo(json.dumps(_linear_client().get_team_states(team_id), indent=2))


@linear.command("members")
@click.option("--team-id", required=True)
def linear_members(team_id: str):
    click.echo(json.dumps(_linear_client().get_team_members(team_id), indent=2))


@linear.command("projects")
@click.option("--team-id", required=True)
def linear_projects(team_id: str):
    click.echo(json.dumps(_linear_client().get_projects(team_id), indent=2))


@linear.command("issues")
@click.option("--team-id", required=True)
@click.option("--first", default=50, type=int, show_default=True)
def linear_issues(team_id: str, first: int):
    click.echo(json.dumps(_linear_client().get_issues(team_id, first=first), indent=2))


@linear.command("get-issue")
@click.option("--issue-id", required=True)
def linear_get_issue(issue_id: str):
    click.echo(json.dumps(_linear_client().get_issue(issue_id), indent=2))


@linear.command("create-issue")
@click.option("--team-id", required=True)
@click.option("--title", required=True)
@click.option("--description", default=None)
@click.option(
    "--priority",
    type=click.Choice(list(LINEAR_PRIORITY)),
    default=None,
    help="Linear priority: urgent, high, normal, or low.",
)
@click.option("--assignee-id", default=None, help="Linear user id to assign the issue to.")
@click.option("--due-date", default=None, help="Due date as an ISO date, e.g. 2026-08-24.")
@click.option("--project-id", default=None)
@click.option("--parent-id", default=None, help="Linear issue id to nest this issue under as a sub-issue.")
def linear_create_issue(
    team_id: str,
    title: str,
    description: str | None,
    priority: str | None,
    assignee_id: str | None,
    due_date: str | None,
    project_id: str | None,
    parent_id: str | None,
):
    issue = _linear_client().create_issue(
        team_id,
        title,
        description,
        priority=LINEAR_PRIORITY[priority] if priority else None,
        assignee_id=assignee_id,
        due_date=due_date,
        project_id=project_id,
        parent_id=parent_id,
    )
    click.echo(json.dumps(issue, indent=2))


@linear.command("set-state")
@click.option("--issue-id", required=True)
@click.option("--state-id", required=True, help="A workflow state id valid for the issue's team.")
def linear_set_state(issue_id: str, state_id: str):
    issue = _linear_client().update_issue_state(issue_id, state_id)
    click.echo(json.dumps(issue, indent=2))


if __name__ == "__main__":
    cli()
