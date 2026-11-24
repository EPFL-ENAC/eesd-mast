env_path=../.env

install:
	uv sync

run:
	uv run --env-file "$(env_path)" uvicorn app.main:app --reload

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

db-upgrade:
	uv run --env-file "$(env_path)" alembic upgrade head

db-downgrade:
	uv run --env-file "$(env_path)" alembic downgrade -1

db-revision:
	uv run --env-file "$(env_path)" alembic revision --autogenerate -m "$(name)"
