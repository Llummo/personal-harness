# personal-harness

Harness I use for ClickUp ticket creation and QA.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -e ".[dev]"
cp .env.example .env   # then fill in CLICKUP_API_TOKEN
```

`CLICKUP_API_TOKEN` is your personal ClickUp API token (ClickUp → Settings →
Apps). `.env` is gitignored — never commit real tokens.

## Usage

```bash
./.venv/bin/harness clickup teams
./.venv/bin/harness clickup spaces --team-id <team_id>
./.venv/bin/harness clickup lists --space-id <space_id>
./.venv/bin/harness clickup create-task --list-id <list_id> --name "Ticket title" --description "..."
```

## Layout

```
src/harness/
  config.py       # env-based config (CLICKUP_API_TOKEN, etc.)
  clickup/        # ClickUp REST API client
  qa/             # placeholder for future QA tooling
  cli.py          # click-based CLI entrypoint
tests/            # pytest + responses (mocked HTTP)
```

## Tests

```bash
./.venv/bin/pytest
```
