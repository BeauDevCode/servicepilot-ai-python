# ServicePilot AI

**Turn messy customer requests into organized jobs, quotes, invoices, and follow-ups.**

ServicePilot AI is a Python-first FastAPI web app for small local service businesses and freelancers. It helps mobile mechanics, cleaners, tutors, landscapers, photographers, handymen, barbers, and student entrepreneurs turn scattered texts, DMs, emails, and phone notes into a usable business workflow.

## What It Proves

- Production-style FastAPI app structure
- Jinja2 templates with HTMX-ready server rendering
- SQLite persistence with SQLModel relationships
- Real CRUD flows for customers, jobs, quotes, invoices, tasks, settings, and analytics
- OpenAI integration through `OPENAI_API_KEY`
- Strong mock AI fallback when no API key exists
- Secure environment variable handling
- Tests with pytest
- Ruff linting
- Docker and Docker Compose
- GitHub Actions CI

## Core Workflow

Paste a messy customer message:

```text
hey bro can you come saturday to fix my brakes i got a 2008 honda accord and it making grinding sound how much
```

ServicePilot AI extracts:

- Customer and contact details
- Service category
- Job title and description
- Vehicle, property, or project details
- Urgency and preferred timing
- Missing information to ask for
- Suggested quote range
- Checklist
- Customer follow-up message

Then it can create a customer, job, quote draft, and follow-up task in one click.

## Tech Stack

- Python 3.11+
- FastAPI
- Jinja2
- HTMX
- Tailwind CSS
- SQLite
- SQLModel
- Pydantic
- OpenAI API
- pytest
- Ruff
- Docker
- GitHub Actions

## Quick Start

```bash
git clone https://github.com/BeauDevCode/servicepilot-ai-python.git
cd servicepilot-ai-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000).

The app seeds demo data automatically when `DEMO_MODE=true`.

## Optional OpenAI Setup

The app works without an API key using deterministic mock extraction. To use real AI extraction:

```bash
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4.1-mini
```

Never commit `.env`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## Tests and Linting

```bash
make lint
make test
```

## Pages

- `/` landing page
- `/dashboard` business dashboard
- `/ai-assistant` AI intake workflow
- `/customers` CRM
- `/jobs` job board
- `/quotes` quote management
- `/invoices` invoice tracking
- `/tasks` follow-up task list
- `/analytics` business insights
- `/settings` business and environment settings

## Security Notes

- API keys are loaded from environment variables.
- `.env` and SQLite databases are ignored by git.
- Real AI output is validated through a Pydantic schema.
- The mock extractor keeps demos safe and repeatable.

## Portfolio Positioning

This is not a generic chatbot. It is a vertical workflow app that shows product thinking, backend design, database modeling, AI integration, UI implementation, operational tooling, and deployment readiness.

## Resume Bullets

- Built ServicePilot AI, a Python FastAPI SaaS MVP that converts messy customer service messages into structured customers, jobs, quote drafts, invoices, tasks, and follow-ups.
- Designed relational SQLModel data models for CRM, job tracking, quotes, invoices, business settings, and task workflows backed by SQLite.
- Integrated OpenAI behind environment-based configuration with a deterministic mock AI fallback for safe demos, local development, and CI.
- Implemented a polished server-rendered dashboard using Jinja2, HTMX-ready forms, Tailwind CSS, and reusable template components.
- Added Docker, Docker Compose, pytest coverage, Ruff linting, GitHub Actions CI, seed data, and professional project documentation.

## Interview Talking Points

- Why this is a workflow product instead of a generic chatbot: AI output becomes durable business records.
- How the mock AI fallback protects demos and CI from external API failures or missing secrets.
- How SQLModel relationships connect customers, jobs, quotes, invoices, and tasks.
- How FastAPI dependencies keep database sessions scoped and testable.
- How the app handles API keys through `.env` and `.gitignore` instead of hardcoded secrets.
- How the dashboard and analytics pages surface operational value for small service businesses.
- What production upgrades would come next: auth, role-based access, migrations, background jobs, email/SMS sending, payments, and deployment observability.
