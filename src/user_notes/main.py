from fastapi import FastAPI

from user_notes.database import Base, engine
from user_notes.models.notes import Notes
from user_notes.models.users import User
from user_notes.routers.notes import router as notes_router
from user_notes.routers.users import router as users_router

app = FastAPI(title="User Notes API")

app.include_router(notes_router)
app.include_router(users_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "Ok"}
