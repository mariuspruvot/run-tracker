from sqlalchemy.orm import Session
from base_repository import AbstractRepository
from backend.models.user import User
from backend.schemas.user import UserCreate, UserResponse
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class UserRepository(AbstractRepository[UserCreate, int]):
    def __init__(self, db: Session):
        self.db = db

    def create(self, instance: UserCreate) -> UserResponse:
        """
        Create a new user instance in the database and return the response object.
        """
        user = User(
            username=instance.username,
            email=instance.email,
            hashed_password=instance.password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User with id {user.id} created")
        return UserResponse.model_validate(user)

    def delete(self, id: int) -> None:
        """
        Delete an existing user instance from the database.
        """
        user = self.get(id)

        if not user:
            logger.error(f"User with id {id} not found")
            return

        self.db.delete(user)
        self.db.commit()
        logger.info(f"User with id {id} deleted")

    def get(self, id: int) -> UserResponse | None:
        """
        Fetch an existing user instance from the database by it's unique id.
        """
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            logger.error(f"User with id {id} not found")
            return None
        return UserResponse.model_validate(user)

    def list(self, limit: int, start: int) -> List[UserResponse]:
        """
        List all existing user instances from the database.
        """
        users = self.db.query(User).offset(start).limit(limit).all()

        if not users:
            logger.error("No users found")
            return []
        return [UserResponse.model_validate(user) for user in users]

    def update(self, id: int, instance: UserCreate) -> UserResponse | None:
        """
        Update an existing user instance in the database.
        """
        user = self.get(id)

        if not user:
            logger.error(f"User with id {id} not found")
            return None

        user.username = instance.username
        user.email = instance.email
        user.hashed_password = instance.password
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User with id {id} updated")
        return UserResponse.model_validate(user)
