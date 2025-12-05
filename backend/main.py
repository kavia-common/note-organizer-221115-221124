from typing import List, Optional, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_TITLE = "Notes Organizer Backend"
APP_DESC = "FastAPI backend providing CRUD operations for notes (in-memory store)"
APP_VERSION = "1.0.0"

# Initialize FastAPI with OpenAPI tags
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESC,
    version=APP_VERSION,
    openapi_tags=[
        {"name": "Health", "description": "Health check endpoint"},
        {"name": "Notes", "description": "CRUD operations for notes (in-memory)"},
    ],
)

# In-memory storage with incremental IDs
_notes_store: Dict[int, Dict] = {}
_next_id: int = 1


class NoteBase(BaseModel):
    """Base fields for a Note."""
    title: str = Field(..., description="Title of the note", min_length=1)
    content: str = Field("", description="Content/body of the note")
    tags: Optional[List[str]] = Field(default_factory=list, description="Optional list of tags")


class NoteCreate(NoteBase):
    """Payload model to create a note."""
    pass


class NoteUpdate(BaseModel):
    """Payload model to update a note (partial allowed)."""
    title: Optional[str] = Field(None, description="Title of the note")
    content: Optional[str] = Field(None, description="Content/body of the note")
    tags: Optional[List[str]] = Field(None, description="Optional list of tags")


class Note(NoteBase):
    """Note response model."""
    id: int = Field(..., description="Unique incremental identifier for the note")


# Enable CORS for frontend - strict to React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health check", description="Returns API health status.")
def health():
    """Health endpoint indicating that the backend service is running."""
    return {"status": "ok", "service": APP_TITLE, "version": APP_VERSION}

# PUBLIC_INTERFACE
@app.get(
    "/notes",
    response_model=List[Note],
    tags=["Notes"],
    summary="List notes",
    description="Returns the list of all notes from the in-memory store.",
)
def list_notes() -> List[Note]:
    """List all notes from the in-memory store."""
    return list(_notes_store.values())

# PUBLIC_INTERFACE
@app.post(
    "/notes",
    response_model=Note,
    tags=["Notes"],
    summary="Create note",
    description="Create a new note with title, content, and optional tags in the in-memory store.",
    status_code=201,
)
def create_note(payload: NoteCreate) -> Note:
    """Create a new note in the in-memory store."""
    global _next_id
    note = {
        "id": _next_id,
        "title": payload.title,
        "content": payload.content,
        "tags": payload.tags or [],
    }
    _notes_store[_next_id] = note
    _next_id += 1
    return note

# PUBLIC_INTERFACE
@app.put(
    "/notes/{note_id}",
    response_model=Note,
    tags=["Notes"],
    summary="Update note",
    description="Update an existing note by ID in the in-memory store.",
)
def update_note(note_id: int, payload: NoteUpdate) -> Note:
    """Update an existing note by ID in the in-memory store."""
    if note_id not in _notes_store:
        raise HTTPException(status_code=404, detail="Note not found")

    note = _notes_store[note_id].copy()
    if payload.title is not None:
        note["title"] = payload.title
    if payload.content is not None:
        note["content"] = payload.content
    if payload.tags is not None:
        note["tags"] = payload.tags

    _notes_store[note_id] = note
    return note

# PUBLIC_INTERFACE
@app.delete(
    "/notes/{note_id}",
    tags=["Notes"],
    summary="Delete note",
    description="Delete an existing note by ID from the in-memory store.",
)
def delete_note(note_id: int):
    """Delete an existing note by ID from the in-memory store."""
    if note_id not in _notes_store:
        raise HTTPException(status_code=404, detail="Note not found")
    del _notes_store[note_id]
    return {"ok": True, "deleted": note_id}

# Note on running:
# Use: uvicorn main:app --host 0.0.0.0 --port 3001 --reload
