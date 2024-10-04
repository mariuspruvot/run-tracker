from fastapi import APIRouter, Depends, HTTPException

from backend.repositories.user_repository import UserRepository
from backend.schemas.user import UserCreate, UserResponse
from backend.settings.base import GLOBAL_SETTINGS
from backend.config.database import get_db
from sqlalchemy.orm import Session

user_router = APIRouter()


@user_router.get("/health-check", tags=["Users"])
def health_check():
    return {"status": "ok"}


@user_router.post("/create", response_model=UserResponse, tags=["Users"])
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user instance in the database and return the response object.
    """
    repository = UserRepository(db)
    try:
        return repository.create(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
