# Contributing

Thanks for taking a look at ServicePilot AI.

## Local setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On Windows PowerShell, use `py -3.12 -m venv .venv` and `.\.venv\Scripts\Activate.ps1` instead of the first two commands. Open `http://localhost:8000` and check `http://localhost:8000/api/health`.

The app seeds fictional records when `DEMO_MODE=true` (the default). Use fake customer details in the shared public demo.

## Checks

Run these before opening a pull request:

```bash
python -m ruff check .
python -m pytest -vv
```

## Good first contributions

Good starter tasks include:

- README improvements
- screenshot updates
- small UI polish
- test coverage
- documentation cleanup
- demo data improvements

## Pull requests

Please include:

- what changed
- why it changed
- how you tested it
- screenshots for UI changes

For data changes, include a test that exercises the affected service or route. Keep database files, `.env`, API keys, and real customer information out of commits.

Keep changes focused and small when possible.
