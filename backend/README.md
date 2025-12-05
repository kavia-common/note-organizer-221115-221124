# Notes Organizer Backend (FastAPI)

Run the backend locally:
- Install: pip install fastapi uvicorn pydantic
- Start: uvicorn main:app --host 0.0.0.0 --port 3001 --reload

Endpoints:
- GET /            -> Health
- GET /notes       -> List all notes
- POST /notes      -> Create a note
- PUT /notes/{id}  -> Update a note
- DELETE /notes/{id} -> Delete a note

CORS is enabled for http://localhost:3000
Storage uses a simple JSON file at backend/data/notes.json
