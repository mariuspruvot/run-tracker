from sqlalchemy.orm import Session

from backend.exceptions.users import UserNotFoundException
from backend.models.user import User
from backend.repositories.base_repository import AbstractRepository
from backend.schemas.user import UserCreate, UserResponse
from typing import List
import bcrypt
import logging
import uuid
from sqlalchemy.dialects.postgresql import UUID


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
            hashed_password=str(
                bcrypt.hashpw(instance.password.encode(), bcrypt.gensalt())
            ),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User with id {user.id} created")
        return UserResponse.model_validate(user)

    def delete(self, id: uuid) -> None:
        """
        Delete an existing user instance from the database.
        """
        user = self.get(id)

        if not user:
            logger.error(f"User with id {id} not found")
            raise UserNotFoundException(f"User with id {id} not found")

        self.db.delete(user)
        self.db.commit()
        logger.info(f"User with id {id} deleted")

    def get(self, id: UUID) -> UserResponse | None:
        """
        Fetch an existing user instance from the database by its unique id.
        """
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            logger.error(f"User with id {id} not found")
            raise UserNotFoundException(f"User with id {id} not found")
        return UserResponse.model_validate(user)

    def list(self, limit: int = 10, start: int = 0) -> List[UserResponse]:
        """
        List all existing user instances from the database.
        """
        users = self.db.query(User).offset(start).limit(limit).all()

        if not users:
            logger.error("No users found")
            raise UserNotFoundException("No users found")
        return [UserResponse.model_validate(user) for user in users]

    def update(self, id: uuid, instance: UserCreate) -> UserResponse | None:
        """
        Update an existing user instance in the database.
        """
        user = self.get(id)

        if not user:
            logger.error(f"User with id {id} not found")
            raise UserNotFoundException(f"User with id {id} not found")

        user.username = instance.username
        user.email = instance.email
        user.hashed_password = str(
            bcrypt.hashpw(instance.password.encode(), bcrypt.gensalt())
        )
        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User with id {id} updated")
        return UserResponse.model_validate(user)
