FROM python:3.12-slim

WORKDIR /app
COPY api /app/api
COPY worker /app/worker
COPY shared /app/shared
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY pyproject.toml /app/pyproject.toml
COPY scripts /app/scripts

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

EXPOSE 8088
