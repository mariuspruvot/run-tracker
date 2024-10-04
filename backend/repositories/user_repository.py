from base_repository import AbstractRepository

from backend.models.user import User
from backend.schemas.user import UserBase

class UserRepository(AbstractRepository[UserBase, int]):
    def create(self, instance: UserBase) -> User:
        pass

    def delete(self, id: int) -> None:
        pass

    def get(self, id: int) -> User:
        pass

    def list(self, limit: int, start: int) -> list[User]:
        pass

    def update(self, id: int, instance: UserBase) -> User:
        pass
