from fastapi import FastAPI

from user_notes.routers.notes import router as notes_router
from user_notes.routers.users import router as users_router

app = FastAPI(title="User Notes API")

app.include_router(notes_router)
app.include_router(users_router)


@app.get("/")
def health_check():
    return {"status": "Ok"}
