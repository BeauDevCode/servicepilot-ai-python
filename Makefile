.PHONY: install dev test lint seed docker

install:
	python -m pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

seed:
	python scripts/seed_db.py

docker:
	docker compose up --build

