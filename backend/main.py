from fastapi import FastAPI
from backend.settings.base import GLOBAL_SETTINGS

app = FastAPI()


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
