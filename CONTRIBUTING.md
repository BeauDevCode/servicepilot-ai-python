# Contributing

Thanks for taking a look at ServicePilot AI.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000`.

## Checks

Run these before opening a pull request:

```bash
ruff check .
pytest -vv
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

Keep changes focused and small when possible.
