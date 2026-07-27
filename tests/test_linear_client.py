import pytest
import responses

from harness.linear import LinearAPIError, LinearClient

API_URL = "https://api.linear.app/graphql"


@responses.activate
def test_get_teams():
    responses.add(
        responses.POST,
        API_URL,
        json={"data": {"teams": {"nodes": [{"id": "t1", "name": "Sigo", "key": "SIG"}]}}},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    teams = client.get_teams()

    assert teams == [{"id": "t1", "name": "Sigo", "key": "SIG"}]


@responses.activate
def test_get_team_states():
    responses.add(
        responses.POST,
        API_URL,
        json={"data": {"team": {"states": {"nodes": [{"id": "s1", "name": "Todo", "type": "unstarted"}]}}}},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    states = client.get_team_states("t1")

    assert states == [{"id": "s1", "name": "Todo", "type": "unstarted"}]


@responses.activate
def test_get_team_members():
    responses.add(
        responses.POST,
        API_URL,
        json={"data": {"team": {"members": {"nodes": [{"id": "u1", "name": "Ana", "email": "a@x.com"}]}}}},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    members = client.get_team_members("t1")

    assert members[0]["email"] == "a@x.com"


@responses.activate
def test_get_issues():
    responses.add(
        responses.POST,
        API_URL,
        json={"data": {"team": {"issues": {"nodes": [{"id": "i1", "identifier": "SIG-1", "title": "Fix"}]}}}},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    issues = client.get_issues("t1")

    assert issues[0]["identifier"] == "SIG-1"


@responses.activate
def test_create_issue_returns_created_issue():
    responses.add(
        responses.POST,
        API_URL,
        json={"data": {"issueCreate": {"success": True, "issue": {"id": "i1", "identifier": "SIG-1"}}}},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    issue = client.create_issue("t1", "Do the thing")

    assert issue["identifier"] == "SIG-1"


@responses.activate
def test_create_issue_raises_when_not_successful():
    responses.add(
        responses.POST,
        API_URL,
        json={"data": {"issueCreate": {"success": False, "issue": None}}},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    with pytest.raises(LinearAPIError, match="issue creation failed"):
        client.create_issue("t1", "Do the thing")


@responses.activate
def test_update_issue_state():
    responses.add(
        responses.POST,
        API_URL,
        json={
            "data": {
                "issueUpdate": {
                    "success": True,
                    "issue": {"id": "i1", "identifier": "SIG-1", "state": {"id": "s2", "name": "Done"}},
                }
            }
        },
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    issue = client.update_issue_state("i1", "s2")

    assert issue["state"]["name"] == "Done"


@responses.activate
def test_graphql_errors_in_200_body_raise():
    # GraphQL reports failures inside a 200 response, so a non-error status
    # alone must not be treated as success.
    responses.add(
        responses.POST,
        API_URL,
        json={"errors": [{"message": "Authentication required"}]},
        status=200,
    )
    client = LinearClient(api_key="fake-key")

    with pytest.raises(LinearAPIError, match="GraphQL error"):
        client.get_teams()


@responses.activate
def test_http_error_raises():
    responses.add(responses.POST, API_URL, json={"error": "nope"}, status=401)
    client = LinearClient(api_key="fake-key")

    with pytest.raises(LinearAPIError, match="401"):
        client.get_teams()
