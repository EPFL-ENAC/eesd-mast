env_path=../.env
data="./scripts/Shake_Table_Tests_Database_v01.xlsx"

install:
	poetry install

run:
	poetry run dotenv -f "$(env_path)" run uvicorn app.main:app --reload

lint:
	poetry run pre-commit run --all-files

db-upgrade:
	poetry run dotenv -f "$(env_path)" run alembic upgrade head

db-downgrade:
	poetry run dotenv -f "$(env_path)" run alembic downgrade -1

db-revision:
	poetry run dotenv -f "$(env_path)" run alembic revision --autogenerate -m "$(name)"

db-seed:
	poetry run dotenv -f "$(env_path)" run python scripts/seed.py $(data)
