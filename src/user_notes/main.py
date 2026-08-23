from fastapi import FastAPI

from user_notes.database import Base,engine
from user_notes.models.notes import Notes
from user_notes.routers.notes import router

app = FastAPI(title="User Notes API")
app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status":"Ok"}