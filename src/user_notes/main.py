from fastapi import FastAPI

from user_notes.routers.notes import router as notes_router
from user_notes.routers.users import router as users_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from user_notes.core.limiter import limiter


app = FastAPI(title="User Notes API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(notes_router)
app.include_router(users_router)


@app.get("/")
def health_check():
    return {"status": "Ok"}
