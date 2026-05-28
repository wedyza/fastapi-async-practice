# Repository Guidelines

## Project Structure & Module Organization
- `src/albot/` holds the application package.
- `tests/` is reserved for pytest tests
- `deploy/Dockerfile` and `compose.yml` define containerized development.
- `pyproject.toml` and `uv.lock` define dependencies and tooling.

## Build, Test, and Development Commands
- `uv sync` installs dependencies into the local virtual environment.
- `uv run uvicorn albotgm.web.app:app --reload` runs the API locally with reload.
- `uv run pytest` runs the test suite.
- `docker compose up --build` builds and runs the service in Docker.
- use `uv add *package_name*` to add a new package followed by `uv sync` to check if everying is correct

## Coding Style & Naming Conventions
- Use 4-space indentation and keep lines at 100 characters (Ruff config).
- Format with `uv run ruff format` and lint with `uv run ruff check`.
- Prefer `snake_case` for modules/functions, `PascalCase` for classes, and `UPPER_CASE` for constants.
- Keep routers in feature folders and export them through `src/albotgm/web/routers/__init__.py`.
- Use Pydantic models over dataclasses
- After finishing main request, run `uv run ruff check --fix` for codestyle matching and `uv run basedpyright` to make sure there are no static typing errors
- If there are static typing errors, fix them before finishing
- Run `uv run pytest --cov` to make sure all tests are passed
- For PostgreSQL 18+, keep the DB volume mount exactly as `pgdata:/var/lib/postgresql` in `compose.yml`; do not change it to `/var/lib/postgresql/data`.

## Testing Guidelines
- Use pytest (`tests/` with files named `test_*.py`).
- Keep tests focused on behavior (API responses, router wiring, and lifespan effects).
- If adding coverage enforcement, use `pytest-cov` (already in dev dependencies).
