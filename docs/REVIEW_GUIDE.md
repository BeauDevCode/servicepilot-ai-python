# Review Guide

This guide is for recruiters, engineers, and reviewers who want to inspect the project quickly.

## What to review first

1. `README.md` for the product summary, screenshots, setup, tests, and Docker instructions.
2. `app/models.py` for the core data model.
3. `app/services/` for workflow logic.
4. `app/routes/` for page and API behavior.
5. `app/ai.py` for the OpenAI integration and deterministic mock mode.
6. `tests/` for coverage around pages, services, analytics, quotes, invoices, tasks, and AI parsing.
7. `.github/workflows/ci.yml` for the automated quality gate.

## Validation commands

```bash
ruff check .
pytest -vv
```

Docker path:

```bash
docker compose up --build
```

## Engineering signals

- FastAPI app structure with separated routes, services, schemas, and models.
- SQLModel-backed persistence with customer, job, quote, invoice, task, and settings workflows.
- Mock AI mode so local development and CI do not depend on an external API key.
- GitHub Actions workflow for linting and tests.
- Docker and Docker Compose setup for repeatable local review.

## Current limitations

- SQLite is used for simple local/demo persistence.
- The UI is server-rendered rather than a separate frontend app.
- The AI flow is intentionally constrained to structured intake rather than broad chat behavior.
- The project is a portfolio MVP, not a production SaaS with auth, billing, or multi-tenant controls.
