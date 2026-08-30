from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from user_notes.database import get_db
from user_notes.schemas.notes import NoteUpdate, NoteCreate, NoteOut
from user_notes.services import notes_service
from user_notes.core.dependencies import get_current_user
from user_notes.models.users import User

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteOut])
def get_notes(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return notes_service.get_notes(db, current_user.id)


@router.post("/", response_model=NoteOut, status_code=201)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return notes_service.create_note(db, note, current_user.id)


@router.post("/search", response_model=list[NoteOut], status_code=200)
def search_note(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return notes_service.search_notes(db, current_user.id, q)


@router.get("/{note_id}", response_model=NoteOut, status_code=200)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = notes_service.get_note(db, note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note Not found")

    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not Authorized to access this note"
        )
    return note


@router.patch("/{note_id}", response_model=NoteOut, status_code=200)
def update_note(
    note_id: int,
    note_schema: NoteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = notes_service.get_note(db, note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note Not Found")

    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not Authorized to access this note"
        )

    return notes_service.update_note(db, note_schema, note_id)


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    note = notes_service.get_note(db, note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note Not Found")

    if note.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not Authorized to access this note"
        )

    notes_service.delete_note(db, note_id)
