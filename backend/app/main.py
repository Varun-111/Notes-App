from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from app.schemas import NoteCreate, NoteRead, NoteUpdate

app = FastAPI(title = "Notes App", description = "A simple notes app built with FastAPI", version = "1.0.0")

db: dict = {"notes": {}, "next_id": 1}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

def get_note_or_404(note_id: int) -> dict:
    note = db["notes"].get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/notes", response_model=NoteRead, status_code=201)
async def create_note(note: NoteCreate):
    now = datetime.now(timezone.utc)
    note_id = db["next_id"]
    db["next_id"] += 1
    stored = {"id": note_id, "title": note.title, "body": note.body, "created_at": now, "updated_at": now}
    db["notes"][note_id] = stored
    return stored

@app.get("/notes", response_model=list[NoteRead])
async def list_notes():
    return list(db["notes"].values())

@app.get("/notes/{note_id}", response_model=NoteRead)
async def get_note(note_id: int):
    return get_note_or_404(note_id)

@app.patch("/notes/{note_id}", response_model=NoteRead)
async def update_note(note_id: int, changes: NoteUpdate):
    stored = get_note_or_404(note_id)
    sent = changes.model_dump(exclude_unset=True)
    stored.update({k:v for k, v in sent.items() if v is not None})
    stored["updated_at"] = datetime.now(timezone.utc)
    return stored

@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int):
    get_note_or_404(note_id)
    del db["notes"][note_id]
