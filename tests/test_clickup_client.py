import pytest
import responses

from harness.clickup import ClickUpClient
from harness.clickup.client import ClickUpAPIError


@responses.activate
def test_get_teams():
    responses.add(
        responses.GET,
        "https://api.clickup.com/api/v2/team",
        json={"teams": [{"id": "123", "name": "My Team"}]},
        status=200,
    )
    client = ClickUpClient(api_token="fake-token")

    teams = client.get_teams()

    assert teams == [{"id": "123", "name": "My Team"}]


@responses.activate
def test_get_task():
    responses.add(
        responses.GET,
        "https://api.clickup.com/api/v2/task/task1",
        json={"id": "task1", "name": "Do the thing"},
        status=200,
    )
    client = ClickUpClient(api_token="fake-token")

    task = client.get_task("task1")

    assert task == {"id": "task1", "name": "Do the thing"}


@responses.activate
def test_get_folders():
    responses.add(
        responses.GET,
        "https://api.clickup.com/api/v2/space/space123/folder",
        json={"folders": [{"id": "folder1", "name": "Project-1"}]},
        status=200,
    )
    client = ClickUpClient(api_token="fake-token")

    folders = client.get_folders("space123")

    assert folders == [{"id": "folder1", "name": "Project-1"}]


@responses.activate
def test_get_tasks():
    responses.add(
        responses.GET,
        "https://api.clickup.com/api/v2/list/list123/task",
        json={"tasks": [{"id": "task1", "name": "Do the thing"}]},
        status=200,
    )
    client = ClickUpClient(api_token="fake-token")

    tasks = client.get_tasks("list123")

    assert tasks == [{"id": "task1", "name": "Do the thing"}]


@responses.activate
def test_create_task():
    responses.add(
        responses.POST,
        "https://api.clickup.com/api/v2/list/list123/task",
        json={"id": "task1", "name": "Do the thing"},
        status=200,
    )
    client = ClickUpClient(api_token="fake-token")

    task = client.create_task("list123", "Do the thing")

    assert task["name"] == "Do the thing"


@responses.activate
def test_update_task_status():
    responses.add(
        responses.PUT,
        "https://api.clickup.com/api/v2/task/task1",
        json={"id": "task1", "status": {"status": "done"}},
        status=200,
    )
    client = ClickUpClient(api_token="fake-token")

    task = client.update_task_status("task1", "done")

    assert task["status"]["status"] == "done"
    assert responses.calls[0].request.body == b'{"status": "done"}'


@responses.activate
def test_update_task_status_raises_on_invalid_status():
    responses.add(
        responses.PUT,
        "https://api.clickup.com/api/v2/task/task1",
        json={"err": "Status not found", "ECODE": "STATUS_002"},
        status=400,
    )
    client = ClickUpClient(api_token="fake-token")

    with pytest.raises(ClickUpAPIError):
        client.update_task_status("task1", "not-a-real-status")
