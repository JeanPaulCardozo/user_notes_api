from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from pydantic_core.core_schema import SerializationInfo
from datetime import datetime
from zoneinfo import ZoneInfo


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class NoteCreate(NoteBase):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteUpdate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def format_to_col(self, value: datetime, info: SerializationInfo) -> datetime:
        return value.astimezone(ZoneInfo("America/Bogota"))

    class Config:
        from_attributes = True
