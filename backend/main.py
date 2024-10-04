from fastapi import FastAPI
from backend.routes.users import user_router

app = FastAPI()
app.include_router(user_router, prefix="/users")


def lifespan():
    print("Startup")
    yield
    print("Shutdown")


@app.get("/health-check")
def health_check():
    return {"status": "ok"}
