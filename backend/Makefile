env_path=../.env
data="./scripts/Shake_Table_Tests_Database_v01.xlsx"

install:
	poetry env use python; poetry install

run:
	poetry env use python; poetry run dotenv -f "$(env_path)" run uvicorn mast.main:app --reload

lint:
	poetry run pre-commit run --all-files

database-upgrade:
	DOTENV_PATH_FOR_DYNACONF="$(env_path)" poetry run alembic upgrade head

database-downgrade:
	DOTENV_PATH_FOR_DYNACONF="$(env_path)" poetry run alembic downgrade -1

database-revision:
	DOTENV_PATH_FOR_DYNACONF="$(env_path)" poetry run alembic revision --autogenerate -m "$(name)"

seed:
	DOTENV_PATH_FOR_DYNACONF="$(env_path)" poetry run python scripts/seed.py $(data)
