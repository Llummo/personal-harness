from click.testing import CliRunner

from harness.cli import cli


class FakeClient:
    def __init__(self):
        self.calls = []

    def create_task(self, list_id, name, description=None, **fields):
        self.calls.append({"list_id": list_id, "name": name, "description": description, **fields})
        return {"id": "task1", "name": name}


def _invoke_create_task(monkeypatch, extra_args):
    fake_client = FakeClient()
    monkeypatch.setattr("harness.cli._client", lambda: fake_client)

    runner = CliRunner()
    result = runner.invoke(
        cli, ["clickup", "create-task", "--list-id", "L1", "--name", "Do the thing", *extra_args]
    )
    return result, fake_client


def test_create_task_priority_urgent_maps_to_1(monkeypatch):
    result, fake_client = _invoke_create_task(monkeypatch, ["--priority", "urgent"])

    assert result.exit_code == 0
    assert fake_client.calls[0]["priority"] == 1


def test_create_task_priority_high_maps_to_2(monkeypatch):
    result, fake_client = _invoke_create_task(monkeypatch, ["--priority", "high"])

    assert result.exit_code == 0
    assert fake_client.calls[0]["priority"] == 2


def test_create_task_priority_normal_maps_to_3(monkeypatch):
    result, fake_client = _invoke_create_task(monkeypatch, ["--priority", "normal"])

    assert result.exit_code == 0
    assert fake_client.calls[0]["priority"] == 3


def test_create_task_priority_low_maps_to_4(monkeypatch):
    result, fake_client = _invoke_create_task(monkeypatch, ["--priority", "low"])

    assert result.exit_code == 0
    assert fake_client.calls[0]["priority"] == 4


def test_create_task_without_priority_sends_no_priority_field(monkeypatch):
    result, fake_client = _invoke_create_task(monkeypatch, [])

    assert result.exit_code == 0
    assert "priority" not in fake_client.calls[0]


def test_create_task_rejects_invalid_priority(monkeypatch):
    result, _ = _invoke_create_task(monkeypatch, ["--priority", "urgentish"])

    assert result.exit_code != 0
