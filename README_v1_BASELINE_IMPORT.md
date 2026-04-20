This branch is the staging branch for the full OSINT Workbench v1 baseline generated from the local repo bundle.

Local artifacts prepared:
- osint-workbench-v1.zip
- osint-workbench-v1 folder

Intended import scope:
- api/
- worker/
- shared/
- frontend/
- infra/
- alembic/
- scripts/
- pyproject.toml
- alembic.ini
- .env.example

Reason this is being staged incrementally:
- the existing repository contains unrelated prior scaffold/history on main
- pushing to a feature branch avoids destructive overwrite
- next step is to import the full generated tree and open a PR
