# ServicePilot AI Case Study

## Problem

Small service businesses often receive job requests through texts, calls, direct messages, and notes. Those requests are easy to lose or misunderstand. ServicePilot turns an unstructured customer request into records that a business can act on: customer, job, quote draft, invoice, and follow-up task.

## Goal

Build a small but reviewable workflow app that shows backend modeling, product thinking, UI flow, validation, and deployment readiness.

## Approach

The app is built around a simple workflow:

1. Capture a messy customer request.
2. Extract useful job details.
3. Create structured records.
4. Let the business review and follow up.

The design keeps the app practical instead of turning it into a broad chat tool. The assistant behavior is limited to intake and record creation.

## Architecture

- FastAPI handles routing and application structure.
- SQLModel defines typed database models.
- SQLite keeps local setup simple.
- Jinja2 templates render the UI.
- Service modules keep business logic separate from route handlers.
- Tests cover key pages, services, totals, and workflow behavior.
- GitHub Actions runs the quality gate.

## Tradeoffs

- SQLite is simple and easy to run, but a production app would likely use PostgreSQL.
- Server-rendered pages keep the stack small, but a larger product might split frontend and backend.
- Mock extraction keeps demos and tests reliable, but production use would need stronger review and monitoring.
- The current app focuses on core workflow before adding auth, billing, teams, or multi-tenant features.

## What this project demonstrates

- Building a full-stack app from a real workflow.
- Designing related data models.
- Separating routes, services, templates, and tests.
- Writing a README that lets reviewers run and inspect the project.
- Using automation and validation instead of relying only on screenshots.

## Next steps

- Add authentication and user-owned workspaces.
- Add PostgreSQL support.
- Add audit history for important record changes.
- Improve mobile layout and keyboard flow.
- Add a short demo video to the README.
- Add export/import flows for customers and jobs.
