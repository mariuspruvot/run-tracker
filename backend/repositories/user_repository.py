from sqlalchemy.orm import Session
from sqlalchemy.orm.sync import update

from backend.exceptions.users import UserNotFoundException
from backend.factory.users import UserFactory
from backend.models.user import User
from backend.repositories.base_repository import AbstractRepository
from backend.schemas.user import UserInDB, UserOutDB, UpdateUserInDB
from typing import List
import logging
import uuid
from sqlalchemy.dialects.postgresql import UUID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserRepository(AbstractRepository[UserInDB, int]):
    def __init__(self, db: Session):
        self.db = db

    def create(self, instance: UserInDB) -> UserOutDB:
        """
        Create a new user instance in the database and return the response object.
        """
        user = UserFactory.create_user_in_db(instance)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User with id {user.id} created")

        return UserOutDB.model_validate(user)

    def delete(self, id: uuid) -> None:
        """
        Delete an existing user instance from the database.
        """
        user = self.db.query(User).filter(User.id == id).first()

        if not user:
            logger.error(f"User with id {id} not found")
            raise UserNotFoundException(f"User with id {id} not found")

        self.db.delete(user)
        self.db.commit()
        logger.info(f"User with id {id} deleted")

    def get(self, id: UUID) -> UserOutDB | None:
        """
        Fetch an existing user instance from the database by its unique id.
        """
        user = self.db.query(User).filter(User.id == id).first()

        if not user:
            logger.error(f"User with id {id} not found")
            raise UserNotFoundException(f"User with id {id} not found")

        return UserOutDB.model_validate(user)

    def list(self, limit: int = 10, start: int = 0) -> List[UserOutDB]:
        """
        List all existing user instances from the database.
        """
        users = self.db.query(User).offset(start).limit(limit).all()

        if not users:
            logger.error("No users found")
            raise UserNotFoundException("No users found")
        return [UserOutDB.model_validate(user) for user in users]

    def update(self, id: uuid.UUID, instance: UpdateUserInDB) -> UserOutDB | None:
        """
        Update an existing user instance in the database.
        """
        user = self.db.query(User).filter(User.id == id).first()

        if not user:
            logger.error(f"User with id {id} not found")
            raise UserNotFoundException(f"User with id {id} not found")

        user = UserFactory.update_user_in_db(user, instance)

        self.db.commit()
        self.db.refresh(user)
        logger.info(f"User with id {id} updated")
        return UserOutDB.model_validate(user)
