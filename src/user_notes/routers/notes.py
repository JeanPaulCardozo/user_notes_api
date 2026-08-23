from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from user_notes.database import get_db
from user_notes.schemas.notes import NoteUpdate, NoteCreate, NoteOut
from user_notes.services import notes_service

router = APIRouter(prefix="/notes",tags=["notes"])

@router.get("/", response_model=list[NoteOut])
def get_notes(db: Session = Depends(get_db)):
    return notes_service.get_notes(db)

@router.post("/",response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return notes_service.create_note(db,note)

@router.get("/{note_id}", response_model=NoteOut, status_code=200)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = notes_service.get_note(db,note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note Not found")

    return note

@router.patch("/{note_id}", response_model=NoteOut, status_code=200)
def update_note(note_id: int, note_schema: NoteUpdate, db: Session = Depends(get_db)):
    note = notes_service.update_note(db,note_schema,note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note Not Found")

    return note

@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note_deleted = notes_service.delete_note(db,note_id)

    if not note_deleted:
        raise HTTPException(status_code=404, detail="Note Not Found")


