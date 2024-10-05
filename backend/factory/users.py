from backend.schemas.user import UserInDB, Birthdate
from backend.models.user import User
import bcrypt


class UserFactory:
    @classmethod
    def create_user_in_db(cls, user: UserInDB) -> User:
        """
        Create a new user instance in the database
        """
        return User(
            username=user.username,
            email=user.email,
            hashed_password=str(
                bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
            ),
            birthdate=cls._format_birthdate(user.additional_information.birthdate),
            phone=user.additional_information.phone,
            address=user.additional_information.address,
            city=user.additional_information.city,
            state=user.additional_information.state,
            country=user.additional_information.country,
            zip_code=user.additional_information.zip_code,
        )

    @classmethod
    def _format_birthdate(cls, birthdate: Birthdate) -> str:
        """
        Set the birthdate of the user instance
        """
        return f"{birthdate.year}-{birthdate.month}-{birthdate.day}"
