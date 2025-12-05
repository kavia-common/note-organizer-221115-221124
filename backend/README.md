# Notes Organizer Backend (FastAPI)

FastAPI backend providing in-memory CRUD operations for notes. No database or file storage is used.

- Port: 3001
- CORS: Allows http://localhost:3000
- Allowed Methods: GET, POST, PUT, DELETE
- OpenAPI docs: http://localhost:3001/docs
- OpenAPI JSON: http://localhost:3001/openapi.json

## Quick Start

Create and activate a virtual environment (optional), install requirements, and run:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 3001 --reload
```

Now open the docs at http://localhost:3001/docs

## Endpoints

- GET /           -> Health check
- GET /notes      -> List notes
- POST /notes     -> Create note { title: string (required), content?: string, tags?: string[] }
- PUT /notes/{id} -> Update note (partial allowed) { title?, content?, tags? }
- DELETE /notes/{id} -> Delete note

## Storage

This service uses an in-memory store (a Python dict) with incremental integer IDs. Data resets when the process restarts. Do not add database code.

## CORS

The app enables CORS for:
- http://localhost:3000

Adjust in main.py origins as needed for your environment.

## Frontend

The React app expects the backend at REACT_APP_API_BASE or REACT_APP_BACKEND_URL, defaulting to http://localhost:3001.
