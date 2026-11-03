from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class NoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    body: str = ""

class NoteUpdate(BaseModel):
    title : str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = None

class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int 
    title: str
    body: str
    created_at: datetime
    updated_at: datetime

# from_attributes=True lets Pydantic read from an object like a database row instead of 
# only a dict.