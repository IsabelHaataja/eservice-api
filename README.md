# eService Workflow API

A modular backend API for handling e-service submissions ("cases") with status workflows.
Built to demonstrate production-style structure: API layer, service layer, and database layer.

## Tech stack
- FastAPI (REST API + OpenAPI docs)
- PostgreSQL (Docker)
- SQLAlchemy (ORM)
- Pydantic (validation + schemas)
- Pytest (API tests)

## Architecture
The codebase is organized by responsibility:

- `app/api/`  
  HTTP layer (FastAPI routers). Contains endpoints and depends on services.
- `app/schemas/`  
  Pydantic models (request/response validation).
- `app/services/`  
  Business logic (create/list/get/update). Keeps API layer thin.
- `app/db/`  
  Database session + SQLAlchemy models.
- `app/core/`  
  Application settings loaded from `.env`.

Request flow:
Client &rarr; Router (`app/api`) &rarr; Service (`app/services`) &rarr; DB (`app/db`)

## Running locally
### 1) Start PostgreSQL (Docker)
```bash
docker compose up -d
```
This starts:
- `db` &rarr; Development database (port 5432)
- `test_db` &rarr; Test database (port 5433)
### 2) Create virtualenv + install deps
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
### 3) Configure environment
```bash
APP_NAME=eservice-workflow-api
APP_VERSION=0.1.1
# Development database
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/eservice
# Test database (used only by pytest)
DATABASE_URL_TEST=postgresql+psycopg://app:app@localhost:5433/eservice_test
```
### 4) Run API
```bash
uvicorn app.main:app --reload
```
Open swagger UI: http://127.0.0.1:8000/docs

## Tests
Run tests:
```bash
pytest -q
```
Tests automatically:
- Override DATABASE_URL
- Use the Docker test_db (port 5433)
- Reset database state between tests
- Never touch the development database

## Implemented endpoints
- POST /api/cases Create a case
- GET /api/cases List cases
- GET /api/cases/{id} Get case by id
- PATCH /api/cases/{id}/status Update case status
- GET /api/version → Application metadata

## Database notes
- Tables are created automatically on startup.
- An index (`ix_cases_status`) is created on `case.status` to support efficient filtering.
- Test database is fully isolated from development database.

