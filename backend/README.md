# Notes Organizer Backend (FastAPI)

FastAPI backend providing CRUD operations for notes with simple JSON-file storage (in-memory-like behavior persisted to disk).

- Port: 3001
- CORS: Allows http://localhost:3000
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

- GET /         -> Health check
- GET /notes    -> List notes
- POST /notes   -> Create note { title: string (required), content?: string, tags?: string[] }
- PUT /notes/{id} -> Update note (partial allowed) { title?, content?, tags? }
- DELETE /notes/{id} -> Delete note

## Storage

Notes are saved to data/notes.json within the backend directory. This acts as a lightweight persistence layer for development. No external DB required.

## CORS

The app enables CORS for:
- http://localhost:3000
- https://localhost:3000

Adjust in main.py origins as needed for your environment.

## Frontend

The React app expects the backend at REACT_APP_API_BASE or REACT_APP_BACKEND_URL, defaulting to http://localhost:3001.
