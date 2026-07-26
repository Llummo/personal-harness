from __future__ import annotations

import requests

API_BASE = "https://api.clickup.com/api/v2"


class ClickUpAPIError(RuntimeError):
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"ClickUp API error {status_code}: {payload}")


class ClickUpClient:
    def __init__(self, api_token: str, base_url: str = API_BASE):
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        # ClickUp personal API tokens go directly in the Authorization
        # header, unlike OAuth tokens which use a "Bearer " prefix.
        self._session.headers.update(
            {"Authorization": api_token, "Content-Type": "application/json"}
        )

    def _request(self, method: str, path: str, **kwargs) -> dict:
        response = self._session.request(method, f"{self._base_url}{path}", **kwargs)
        if not response.ok:
            raise ClickUpAPIError(response.status_code, response.json())
        return response.json()

    def get_teams(self) -> list[dict]:
        return self._request("GET", "/team")["teams"]

    def get_spaces(self, team_id: str) -> list[dict]:
        return self._request("GET", f"/team/{team_id}/space")["spaces"]

    def get_folders(self, space_id: str) -> list[dict]:
        return self._request("GET", f"/space/{space_id}/folder")["folders"]

    def get_lists(self, *, space_id: str | None = None, folder_id: str | None = None) -> list[dict]:
        if folder_id:
            return self._request("GET", f"/folder/{folder_id}/list")["lists"]
        if space_id:
            return self._request("GET", f"/space/{space_id}/list")["lists"]
        raise ValueError("Provide either space_id or folder_id")

    def get_task(self, task_id: str) -> dict:
        return self._request("GET", f"/task/{task_id}")

    def get_tasks(self, list_id: str) -> list[dict]:
        return self._request("GET", f"/list/{list_id}/task")["tasks"]

    def create_task(
        self,
        list_id: str,
        name: str,
        description: str | None = None,
        **fields,
    ) -> dict:
        body = {"name": name, "description": description or "", **fields}
        return self._request("POST", f"/list/{list_id}/task", json=body)
