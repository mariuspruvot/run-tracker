from fastapi import FastAPI
from backend.settings.base import GLOBAL_SETTINGS
app = FastAPI()

@app.get("/")
def read_root():
    return {"Database URL": GLOBAL_SETTINGS.get_database_url()}

@app.get("/health-check")
def health_check():
    return {"status": "ok"}
