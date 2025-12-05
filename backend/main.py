from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
import json
from pathlib import Path

APP_TITLE = "Notes Organizer Backend"
APP_DESC = "FastAPI backend providing CRUD operations for notes"
APP_VERSION = "1.0.0"

app = FastAPI(title=APP_TITLE, description=APP_DESC, version=APP_VERSION,
              openapi_tags=[
                  {"name": "Health", "description": "Health check endpoint"},
                  {"name": "Notes", "description": "CRUD operations for notes"}
              ])

# Simple file storage (JSON)
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE = DATA_DIR / "notes.json"

def _load_notes() -> List[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []

def _save_notes(notes: List[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


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
    id: str = Field(..., description="Unique identifier for the note")


# Enable CORS for frontend
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PUBLIC_INTERFACE
@app.get("/", tags=["Health"], summary="Health check", description="Returns API health status.")
def health():
    """Health endpoint indicating that the backend service is running."""
    return {"status": "ok", "service": APP_TITLE, "version": APP_VERSION}

# PUBLIC_INTERFACE
@app.get("/notes", response_model=List[Note], tags=["Notes"], summary="List notes", description="Returns the list of all notes.")
def list_notes():
    """List all notes."""
    return _load_notes()

# PUBLIC_INTERFACE
@app.post("/notes", response_model=Note, tags=["Notes"], summary="Create note", description="Create a new note with title, content, and optional tags.", status_code=201)
def create_note(payload: NoteCreate):
    """Create a new note."""
    notes = _load_notes()
    new_note = {
        "id": str(uuid4()),
        "title": payload.title,
        "content": payload.content,
        "tags": payload.tags or [],
    }
    notes.insert(0, new_note)
    _save_notes(notes)
    return new_note

# PUBLIC_INTERFACE
@app.put("/notes/{note_id}", response_model=Note, tags=["Notes"], summary="Update note", description="Update an existing note by ID.")
def update_note(note_id: str, payload: NoteUpdate):
    """Update an existing note by ID."""
    notes = _load_notes()
    for idx, n in enumerate(notes):
        if n.get("id") == note_id:
            if payload.title is not None:
                n["title"] = payload.title
            if payload.content is not None:
                n["content"] = payload.content
            if payload.tags is not None:
                n["tags"] = payload.tags
            notes[idx] = n
            _save_notes(notes)
            return n
    raise HTTPException(status_code=404, detail="Note not found")

# PUBLIC_INTERFACE
@app.delete("/notes/{note_id}", tags=["Notes"], summary="Delete note", description="Delete an existing note by ID.")
def delete_note(note_id: str):
    """Delete an existing note by ID."""
    notes = _load_notes()
    filtered = [n for n in notes if n.get("id") != note_id]
    if len(filtered) == len(notes):
        raise HTTPException(status_code=404, detail="Note not found")
    _save_notes(filtered)
    return {"ok": True, "deleted": note_id}
