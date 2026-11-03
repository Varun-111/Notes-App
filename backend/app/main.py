from typing import Annotated
from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Note
from app.schemas import NoteCreate, NoteRead, NoteUpdate

app = FastAPI(title = "Notes App", description = "A simple notes app built with FastAPI", version = "1.0.0")

DbSession = Annotated[AsyncSession, Depends(get_db)]

@app.get("/health")
async def health_check():
    return {"status": "ok"}

async def get_note_or_404(db: AsyncSession, note_id: int) -> Note:
    note = await db.get(Note, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/notes", response_model=NoteRead, status_code=201)
async def create_note(data: NoteCreate, db: DbSession):
    note = Note(**data.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note

@app.get("/notes", response_model=list[NoteRead])
async def list_notes(db: DbSession):
    result = await db.execute(select(Note).order_by(Note.id))
    notes = result.scalars().all()
    print("Varun: ", notes)
    return notes

@app.get("/notes/{note_id}", response_model=NoteRead)
async def get_note(note_id: int, db:DbSession):
    return await get_note_or_404(db, note_id)

@app.patch("/notes/{note_id}", response_model=NoteRead)
async def update_note(note_id: int, changes: NoteUpdate, db: DbSession):
    note = await get_note_or_404(db, note_id)
    for field, value in changes.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(note, field, value)
    await db.commit()
    print("Varun: ", note)
    await db.refresh(note)
    return note
    
@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, db: DbSession):
    note = await get_note_or_404(db, note_id)
    await db.delete(note)
    await db.commit()
