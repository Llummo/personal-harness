import responses

from harness.clickup import ClickUpClient


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
