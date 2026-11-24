FROM python:3.14-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /bin/
ENV PYTHONPATH="$PYTHONPATH:/app" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y g++ libpq-dev libgl1
COPY uv.lock pyproject.toml /app/
RUN uv sync --locked --no-dev

COPY alembic.ini prestart.sh /app/
COPY migrations /app/migrations
COPY app /app/app

ENTRYPOINT sh prestart.sh
