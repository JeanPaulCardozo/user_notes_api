from sqlalchemy.orm import Session

from user_notes.models.notes import Notes
from user_notes.schemas.notes import NoteCreate, NoteUpdate


def create_note(db: Session, note_schema: NoteCreate, owner_id: int) -> Notes:
    new_note = Notes(
        title=note_schema.title, content=note_schema.content, owner_id=owner_id
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


def get_notes(db: Session, owner_id: int) -> list[Notes]:
    return db.query(Notes).filter(Notes.owner_id == owner_id).all()


def get_note(db: Session, note_id: int) -> Notes | None:
    return db.query(Notes).filter(Notes.id == note_id).first()


def update_note(db: Session, note_schema: NoteUpdate, note_id: int) -> Notes | None:
    note = get_note(db, note_id)

    if note is None:
        return None

    data = note_schema.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note


def delete_note(db: Session, note_id: int) -> bool:
    note = get_note(db, note_id)

    if note is None:
        return False

    db.delete(note)
    db.commit()

    return True
