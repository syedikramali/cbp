from fastapi import FastAPI
from app.api import payments
from app.utils import events

app = FastAPI()

app.include_router(payments.router, prefix="/api")
app.include_router(events.router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "ok"}
