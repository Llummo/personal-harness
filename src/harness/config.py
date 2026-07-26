import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    clickup_api_token: str
    clickup_team_id: str | None
    clickup_list_id: str | None

    @classmethod
    def from_env(cls) -> "Config":
        token = os.environ.get("CLICKUP_API_TOKEN")
        if not token:
            raise RuntimeError(
                "CLICKUP_API_TOKEN is not set. Copy .env.example to .env and fill it in."
            )
        return cls(
            clickup_api_token=token,
            clickup_team_id=os.environ.get("CLICKUP_TEAM_ID") or None,
            clickup_list_id=os.environ.get("CLICKUP_LIST_ID") or None,
        )
