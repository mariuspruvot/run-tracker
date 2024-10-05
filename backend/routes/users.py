from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic_core.core_schema import json_schema

from backend.exceptions.users import UserNotFoundException
from backend.repositories.user_repository import UserRepository
from backend.schemas.user import UserInDB, UserOutDB, UpdateUserInDB
from backend.config.database import get_db
from sqlalchemy.orm import Session
import uuid

user_router = APIRouter()


@user_router.get("/health-check", tags=["Users"])
def health_check():
    return {"status": "ok"}


@user_router.post("/create", response_model=UserOutDB, tags=["Users"])
async def create_user(user: UserInDB, db: Session = Depends(get_db)):
    """
    Create a new user instance in the database and return the response object.
    """
    repository = UserRepository(db)
    try:
        return repository.create(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/delete/{id}", tags=["Users"])
async def delete_user(id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Delete an existing user instance from the database.
    """
    repository = UserRepository(db)
    try:
        repository.delete(id)
        return Response(status_code=200)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/get/{id}", response_model=UserOutDB, tags=["Users"])
async def get_user(id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Fetch an existing user instance from the database by its unique id.
    """
    repository = UserRepository(db)
    try:
        return repository.get(id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/", response_model=list[UserOutDB], tags=["Users"])
async def get_all_users(db: Session = Depends(get_db)):
    """
    Fetch all existing user instances from the database.
    """
    repository = UserRepository(db)
    try:
        return repository.list()

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.patch("/{id}", response_model=UserOutDB, tags=["Users"])
async def update_user(
    id: uuid.UUID, user: UpdateUserInDB, db: Session = Depends(get_db)
):
    """
    Update an existing user instance in the database.
    """
    repository = UserRepository(db)
    try:
        return repository.update(id, user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
