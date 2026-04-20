# OSINT Workbench v1

A fully wired baseline investigative workbench with:

- FastAPI control plane
- PostgreSQL canonical storage
- Redis + Celery async execution
- MinIO raw/derived artifact storage
- Neo4j derived graph projection
- React/Vite analyst UI
- Alembic migrations
- Real connector contract + normalization pipeline
- Timeline, graph, contradictions, and report artifact generation

## Stack

- API: FastAPI
- Worker: Celery
- DB: PostgreSQL 16
- Cache/Broker: Redis 7
- Object Storage: MinIO
- Graph: Neo4j 5
- Frontend: React + Vite
- Reverse proxy: Nginx

## Quick start

```bash
cp .env.example .env
docker compose -f infra/compose/docker-compose.yml up --build
```

Services:

- API docs: http://localhost:8088/docs
- Frontend: http://localhost:3000
- MinIO console: http://localhost:9001
- Neo4j browser: http://localhost:7474

## Default dev login

The API currently ships with local JWT auth and bootstrap seed settings. Create a user via:

```bash
curl -X POST http://localhost:8088/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"ChangeMe123!","full_name":"Admin"}'
```

Then login:

```bash
curl -X POST http://localhost:8088/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"ChangeMe123!"}'
```

## Notes

This baseline is intentionally connector-safe by default:
- The built-in `manual_import` connector is fully operational.
- HTTP-based enrichers for `ipinfo` and `shodan` are wired and work when valid API keys are supplied.
- Social connectors can be added behind the same contract without changing the pipeline architecture.

## Repo layout

See folders:
- `api/`
- `worker/`
- `frontend/`
- `infra/`
- `alembic/`
- `scripts/`
